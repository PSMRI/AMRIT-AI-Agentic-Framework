from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "config" / "amrit-repositories.txt"


def load_script(module_name: str, filename: str) -> ModuleType:
    script_path = REPOSITORY_ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    # Register before execution so dataclasses can resolve the module.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


clone = load_script("test_clone_amrit_repos", "clone-amrit-repos.py")


def git(arguments: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=str(cwd),
        check=True,
        text=True,
        capture_output=True,
    )


def create_source_repository(root: Path, name: str) -> Path:
    """Create a local Git repository usable as an offline clone source."""

    source = root / name
    source.mkdir(parents=True)
    git(["init", "--initial-branch=main"], cwd=source)
    git(["config", "user.email", "bootstrap-test@example.invalid"], cwd=source)
    git(["config", "user.name", "Bootstrap Test"], cwd=source)
    (source / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    git(["add", "README.md"], cwd=source)
    git(["commit", "-m", "initial commit"], cwd=source)
    return source


def manifest_line(path: str, source: Path) -> str:
    return f"{path}|{source.as_uri()}"


class ManifestParsingTests(unittest.TestCase):
    def test_parses_entries_and_ignores_comments_and_blank_lines(self) -> None:
        entries = clone.parse_manifest(
            "# a comment\n"
            "\n"
            "PSMRI/Common-API|https://github.com/PSMRI/Common-API.git\n"
            "   \n"
            "  PSMRI/HWC-UI | https://github.com/PSMRI/HWC-UI.git  \n"
        )

        self.assertEqual(
            [entry.path for entry in entries], ["PSMRI/Common-API", "PSMRI/HWC-UI"]
        )
        self.assertEqual(entries[1].url, "https://github.com/PSMRI/HWC-UI.git")
        self.assertEqual(entries[0].organization, "PSMRI")
        self.assertEqual(entries[0].name, "Common-API")

    def test_rejects_a_line_without_a_separator(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest("PSMRI/Common-API https://example.invalid/x.git\n")

    def test_rejects_a_line_with_too_many_separators(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest("PSMRI/Common-API|https://x.invalid|extra\n")

    def test_rejects_an_empty_clone_url(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest("PSMRI/Common-API|\n")

    def test_rejects_a_path_without_an_organization(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest("Common-API|https://example.invalid/x.git\n")

    def test_rejects_a_traversing_path(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest("../escape|https://example.invalid/x.git\n")

    def test_rejects_duplicate_repository_paths(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest(
                "PSMRI/Common-API|https://example.invalid/a.git\n"
                "PSMRI/Common-API|https://example.invalid/b.git\n"
            )

    def test_rejects_a_manifest_with_no_entries(self) -> None:
        with self.assertRaises(clone.ManifestError):
            clone.parse_manifest("# only comments\n\n")

    def test_missing_manifest_file_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(clone.ManifestError):
                clone.read_manifest(Path(temporary) / "absent.txt")


class SelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = clone.parse_manifest(
            "PSMRI/Common-API|https://example.invalid/Common-API.git\n"
            "PSMRI/HWC-UI|https://example.invalid/HWC-UI.git\n"
        )

    def test_no_selector_returns_every_entry(self) -> None:
        selected, unmatched = clone.select_entries(self.entries, [])
        self.assertEqual(len(selected), 2)
        self.assertEqual(unmatched, [])

    def test_selects_by_bare_repository_name_case_insensitively(self) -> None:
        selected, unmatched = clone.select_entries(self.entries, ["common-api"])
        self.assertEqual([entry.path for entry in selected], ["PSMRI/Common-API"])
        self.assertEqual(unmatched, [])

    def test_selects_by_organization_qualified_path(self) -> None:
        selected, _ = clone.select_entries(self.entries, ["PSMRI/HWC-UI"])
        self.assertEqual([entry.path for entry in selected], ["PSMRI/HWC-UI"])

    def test_reports_an_unknown_selector(self) -> None:
        selected, unmatched = clone.select_entries(self.entries, ["Nope-API"])
        self.assertEqual(selected, [])
        self.assertEqual(unmatched, ["Nope-API"])


class CloneBehaviourTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.sources = self.root / "sources"
        self.sources.mkdir()
        self.workspace = self.root / "repos"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_clone(self, manifest_text: str, workspace: Path | None = None) -> int:
        manifest = self.root / "manifest.txt"
        manifest.write_text(manifest_text, encoding="utf-8")
        return clone.main(
            [
                "--manifest",
                str(manifest),
                "--workspace",
                str(workspace or self.workspace),
            ]
        )

    def test_case_a_missing_repository_is_cloned_into_the_org_directory(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        status = self.run_clone(manifest_line("PSMRI/Common-API", source) + "\n")

        destination = self.workspace / "PSMRI" / "Common-API"
        self.assertEqual(status, 0)
        self.assertTrue((destination / "README.md").is_file())
        self.assertTrue(clone.is_git_repository(destination))

    def test_case_b_existing_repository_is_skipped_and_left_untouched(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        manifest_text = manifest_line("PSMRI/Common-API", source) + "\n"
        self.assertEqual(self.run_clone(manifest_text), 0)

        destination = self.workspace / "PSMRI" / "Common-API"
        git(["checkout", "-b", "feature/example"], cwd=destination)
        (destination / "work-in-progress.txt").write_text("local work", encoding="utf-8")

        self.assertEqual(self.run_clone(manifest_text), 0)

        branch = git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=destination)
        self.assertEqual(branch.stdout.strip(), "feature/example")
        self.assertEqual(
            (destination / "work-in-progress.txt").read_text(encoding="utf-8"),
            "local work",
        )

    def test_case_b_existing_repository_is_not_updated_from_its_remote(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        manifest_text = manifest_line("PSMRI/Common-API", source) + "\n"
        self.assertEqual(self.run_clone(manifest_text), 0)

        destination = self.workspace / "PSMRI" / "Common-API"
        head_before = git(["rev-parse", "HEAD"], cwd=destination).stdout.strip()

        (source / "added-upstream.txt").write_text("upstream", encoding="utf-8")
        git(["add", "added-upstream.txt"], cwd=source)
        git(["commit", "-m", "upstream commit"], cwd=source)

        self.assertEqual(self.run_clone(manifest_text), 0)

        head_after = git(["rev-parse", "HEAD"], cwd=destination).stdout.strip()
        self.assertEqual(head_before, head_after)
        self.assertFalse((destination / "added-upstream.txt").exists())

    def test_case_c_existing_non_git_path_fails_without_being_touched(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        destination = self.workspace / "PSMRI" / "Common-API"
        destination.mkdir(parents=True)
        (destination / "not-a-repo.txt").write_text("keep me", encoding="utf-8")

        status = self.run_clone(manifest_line("PSMRI/Common-API", source) + "\n")

        self.assertEqual(status, 1)
        self.assertTrue((destination / "not-a-repo.txt").is_file())
        self.assertEqual(
            (destination / "not-a-repo.txt").read_text(encoding="utf-8"), "keep me"
        )
        self.assertFalse((destination / ".git").exists())

    def test_case_d_a_clone_failure_does_not_stop_the_other_repositories(self) -> None:
        good = create_source_repository(self.sources, "HWC-API")
        missing = self.sources / "Absent-API"

        status = self.run_clone(
            manifest_line("PSMRI/Absent-API", missing)
            + "\n"
            + manifest_line("PSMRI/HWC-API", good)
            + "\n"
        )

        self.assertEqual(status, 1)
        self.assertFalse((self.workspace / "PSMRI" / "Absent-API").exists())
        self.assertTrue(
            clone.is_git_repository(self.workspace / "PSMRI" / "HWC-API")
        )

    def test_rerunning_after_a_partial_failure_clones_only_what_is_missing(
        self,
    ) -> None:
        good = create_source_repository(self.sources, "HWC-API")
        later = create_source_repository(self.sources, "TM-API")

        first = self.run_clone(
            manifest_line("PSMRI/HWC-API", good)
            + "\n"
            + manifest_line("PSMRI/Absent-API", self.sources / "Absent-API")
            + "\n"
        )
        self.assertEqual(first, 1)

        second = self.run_clone(
            manifest_line("PSMRI/HWC-API", good)
            + "\n"
            + manifest_line("PSMRI/TM-API", later)
            + "\n"
        )
        self.assertEqual(second, 0)
        self.assertTrue(clone.is_git_repository(self.workspace / "PSMRI" / "TM-API"))

    def test_clones_into_a_workspace_path_containing_spaces(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        workspace = self.root / "a workspace with spaces" / "repos"

        status = self.run_clone(
            manifest_line("PSMRI/Common-API", source) + "\n", workspace=workspace
        )

        self.assertEqual(status, 0)
        self.assertTrue(
            clone.is_git_repository(workspace / "PSMRI" / "Common-API")
        )

    def test_a_cloned_repository_keeps_its_own_origin(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        self.assertEqual(
            self.run_clone(manifest_line("PSMRI/Common-API", source) + "\n"), 0
        )

        destination = self.workspace / "PSMRI" / "Common-API"
        remote = git(["remote", "get-url", "origin"], cwd=destination).stdout.strip()
        self.assertEqual(remote, source.as_uri())

    def test_a_cloned_repository_has_full_history_not_a_shallow_clone(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        self.assertEqual(
            self.run_clone(manifest_line("PSMRI/Common-API", source) + "\n"), 0
        )

        destination = self.workspace / "PSMRI" / "Common-API"
        shallow = git(
            ["rev-parse", "--is-shallow-repository"], cwd=destination
        ).stdout.strip()
        self.assertEqual(shallow, "false")

    def test_dry_run_reports_without_creating_a_clone(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        manifest = self.root / "manifest.txt"
        manifest.write_text(
            manifest_line("PSMRI/Common-API", source) + "\n", encoding="utf-8"
        )

        status = clone.main(
            [
                "--manifest",
                str(manifest),
                "--workspace",
                str(self.workspace),
                "--dry-run",
            ]
        )

        self.assertEqual(status, 0)
        self.assertFalse((self.workspace / "PSMRI" / "Common-API").exists())

    def test_list_reports_invalid_paths_with_a_non_zero_status(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        manifest = self.root / "manifest.txt"
        manifest.write_text(
            manifest_line("PSMRI/Common-API", source) + "\n", encoding="utf-8"
        )
        destination = self.workspace / "PSMRI" / "Common-API"
        destination.mkdir(parents=True)

        status = clone.main(
            [
                "--manifest",
                str(manifest),
                "--workspace",
                str(self.workspace),
                "--list",
            ]
        )
        self.assertEqual(status, 1)

    def test_an_unknown_selector_fails_before_anything_is_cloned(self) -> None:
        source = create_source_repository(self.sources, "Common-API")
        manifest = self.root / "manifest.txt"
        manifest.write_text(
            manifest_line("PSMRI/Common-API", source) + "\n", encoding="utf-8"
        )

        status = clone.main(
            [
                "--manifest",
                str(manifest),
                "--workspace",
                str(self.workspace),
                "No-Such-API",
            ]
        )

        self.assertEqual(status, 1)
        self.assertFalse((self.workspace / "PSMRI").exists())


class CommittedManifestTests(unittest.TestCase):
    def test_the_committed_manifest_parses(self) -> None:
        entries = clone.read_manifest(MANIFEST_PATH)
        self.assertGreater(len(entries), 0)

    def test_every_entry_uses_the_psmri_organization_and_https(self) -> None:
        for entry in clone.read_manifest(MANIFEST_PATH):
            with self.subTest(repository=entry.path):
                self.assertEqual(entry.organization, "PSMRI")
                self.assertTrue(
                    entry.url.startswith("https://github.com/PSMRI/"),
                    f"{entry.path} does not use the documented HTTPS clone style",
                )
                self.assertTrue(entry.url.endswith(f"/{entry.name}.git"))

    def test_no_entry_embeds_credentials_in_its_url(self) -> None:
        for entry in clone.read_manifest(MANIFEST_PATH):
            with self.subTest(repository=entry.path):
                self.assertNotIn("@", entry.url)
                self.assertNotIn("token", entry.url.lower())


class WorkspaceIgnoreTests(unittest.TestCase):
    """The outer repository must never track the developer workspace."""

    def check_ignore(self, relative_path: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "check-ignore", "-v", "--no-index", relative_path],
            cwd=str(REPOSITORY_ROOT),
            check=False,
            text=True,
            capture_output=True,
        )

    def test_the_workspace_directory_is_ignored(self) -> None:
        completed = self.check_ignore("repos/PSMRI/Common-API/pom.xml")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("/repos/", completed.stdout)

    def test_the_ignore_rule_is_root_anchored(self) -> None:
        completed = self.check_ignore("skills/example/repos/notes.md")
        self.assertNotEqual(
            completed.returncode,
            0,
            "A nested directory named 'repos' must not be ignored",
        )


if __name__ == "__main__":
    unittest.main()
