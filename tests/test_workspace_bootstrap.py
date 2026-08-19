from __future__ import annotations

import contextlib
import importlib.util
import io
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


class CloneUrlParsingTests(unittest.TestCase):
    def test_parses_a_github_https_url_with_a_git_suffix(self) -> None:
        self.assertEqual(
            clone.parse_clone_url("https://github.com/PSMRI/Some-New-Repo.git"),
            ("PSMRI", "Some-New-Repo"),
        )

    def test_parses_a_github_https_url_without_a_git_suffix(self) -> None:
        self.assertEqual(
            clone.parse_clone_url("https://github.com/PSMRI/Some-New-Repo"),
            ("PSMRI", "Some-New-Repo"),
        )

    def test_parses_a_url_for_another_organization(self) -> None:
        self.assertEqual(
            clone.parse_clone_url("https://github.com/SomeOrg/Some-Repo.git"),
            ("SomeOrg", "Some-Repo"),
        )

    def test_parses_ssh_scp_syntax(self) -> None:
        self.assertEqual(
            clone.parse_clone_url("git@github.com:PSMRI/Some-New-Repo.git"),
            ("PSMRI", "Some-New-Repo"),
        )

    def test_tolerates_a_trailing_slash(self) -> None:
        self.assertEqual(
            clone.parse_clone_url("https://github.com/PSMRI/Some-New-Repo/"),
            ("PSMRI", "Some-New-Repo"),
        )

    def test_rejects_an_empty_url(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("   ")

    def test_rejects_a_url_without_a_scheme(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("not-a-url")

    def test_rejects_a_url_with_only_one_path_segment(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("https://github.com/OnlyOneSegment.git")

    def test_rejects_a_url_with_no_path_at_all(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("https://github.com")

    def test_rejects_traversal_segments_anywhere_in_the_path(self) -> None:
        for url in (
            "https://github.com/PSMRI/../../etc/passwd",
            "https://github.com/PSMRI/..",
            "https://github.com/./Some-Repo",
        ):
            with self.subTest(url=url):
                with self.assertRaises(clone.AdHocRepositoryError):
                    clone.parse_clone_url(url)

    def test_rejects_percent_encoded_segments(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("https://github.com/PSMRI/%2e%2e")

    def test_rejects_backslash_separators(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("https://github.com/PSMRI\\Some-Repo")

    def test_rejects_whitespace_in_the_url(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("https://github.com/PSMRI/Some Repo.git")

    def test_rejects_an_unsupported_scheme(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.parse_clone_url("ftp://github.com/PSMRI/Some-Repo.git")

    def test_rejects_a_url_with_an_inline_username_and_password(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError) as raised:
            clone.parse_clone_url("https://user:s3cret@github.com/PSMRI/Repo.git")
        self.assertNotIn("s3cret", str(raised.exception))

    def test_rejects_a_url_with_an_inline_token(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError) as raised:
            clone.parse_clone_url("https://ghp_tokenvalue@github.com/PSMRI/Repo.git")
        self.assertNotIn("ghp_tokenvalue", str(raised.exception))

    def test_rejects_ssh_syntax_carrying_a_password(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError) as raised:
            clone.parse_clone_url("git:s3cret@github.com:PSMRI/Repo.git")
        self.assertNotIn("s3cret", str(raised.exception))


class ExplicitWorkspacePathTests(unittest.TestCase):
    def test_accepts_an_organization_and_repository(self) -> None:
        self.assertEqual(
            clone.split_workspace_path("PSMRI/Some-New-Repo"),
            ("PSMRI", "Some-New-Repo"),
        )

    def test_rejects_traversal(self) -> None:
        for candidate in ("../outside", "PSMRI/../repo", "../../PSMRI/repo"):
            with self.subTest(path=candidate):
                with self.assertRaises(clone.AdHocRepositoryError):
                    clone.split_workspace_path(candidate)

    def test_rejects_an_absolute_path(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.split_workspace_path("/repo")

    def test_rejects_a_path_without_an_organization(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.split_workspace_path("repo-only-without-org")

    def test_rejects_a_backslash_separator(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.split_workspace_path("PSMRI\\repo")

    def test_rejects_an_empty_path(self) -> None:
        with self.assertRaises(clone.AdHocRepositoryError):
            clone.split_workspace_path("   ")


class AdHocCloneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.sources = self.root / "sources"
        self.sources.mkdir()
        self.workspace = self.root / "repos"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def adhoc(self, url: str, *extra: str) -> int:
        return clone.main(
            ["--workspace", str(self.workspace), "--url", url, *extra]
        )

    def create_adhoc_source(self) -> tuple[Path, str]:
        """A local repository whose URL derives to PSMRI/Some-New-Repo."""

        source = create_source_repository(self.sources / "PSMRI", "Some-New-Repo")
        return source, source.as_uri()

    def test_clones_to_the_destination_derived_from_the_url(self) -> None:
        _, url = self.create_adhoc_source()

        status = self.adhoc(url)

        destination = self.workspace / "PSMRI" / "Some-New-Repo"
        self.assertEqual(status, 0)
        self.assertTrue(clone.is_git_repository(destination))
        self.assertTrue((destination / "README.md").is_file())

    def test_the_ad_hoc_clone_keeps_its_own_origin(self) -> None:
        _, url = self.create_adhoc_source()
        self.assertEqual(self.adhoc(url), 0)

        destination = self.workspace / "PSMRI" / "Some-New-Repo"
        remote = git(["remote", "get-url", "origin"], cwd=destination).stdout.strip()
        self.assertEqual(remote, url)

    def test_the_ad_hoc_clone_has_full_history(self) -> None:
        _, url = self.create_adhoc_source()
        self.assertEqual(self.adhoc(url), 0)

        destination = self.workspace / "PSMRI" / "Some-New-Repo"
        shallow = git(
            ["rev-parse", "--is-shallow-repository"], cwd=destination
        ).stdout.strip()
        self.assertEqual(shallow, "false")

    def test_an_explicit_path_overrides_the_derived_destination(self) -> None:
        _, url = self.create_adhoc_source()

        status = self.adhoc(url, "--path", "Custom-Org/Renamed-Repo")

        self.assertEqual(status, 0)
        self.assertTrue(
            clone.is_git_repository(self.workspace / "Custom-Org" / "Renamed-Repo")
        )
        self.assertFalse((self.workspace / "PSMRI").exists())

    def test_an_existing_git_repository_is_skipped_and_left_untouched(self) -> None:
        _, url = self.create_adhoc_source()
        self.assertEqual(self.adhoc(url), 0)

        destination = self.workspace / "PSMRI" / "Some-New-Repo"
        git(["checkout", "-b", "feature/local-work"], cwd=destination)
        (destination / "wip.txt").write_text("local work", encoding="utf-8")
        head_before = git(["rev-parse", "HEAD"], cwd=destination).stdout.strip()

        self.assertEqual(self.adhoc(url), 0)

        branch = git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=destination)
        self.assertEqual(branch.stdout.strip(), "feature/local-work")
        self.assertEqual(
            (destination / "wip.txt").read_text(encoding="utf-8"), "local work"
        )
        self.assertEqual(
            git(["rev-parse", "HEAD"], cwd=destination).stdout.strip(), head_before
        )

    def test_an_existing_non_git_path_fails_without_being_touched(self) -> None:
        _, url = self.create_adhoc_source()
        destination = self.workspace / "PSMRI" / "Some-New-Repo"
        destination.mkdir(parents=True)
        (destination / "keep.txt").write_text("keep me", encoding="utf-8")

        status = self.adhoc(url)

        self.assertEqual(status, 1)
        self.assertEqual(
            (destination / "keep.txt").read_text(encoding="utf-8"), "keep me"
        )
        self.assertFalse((destination / ".git").exists())

    def test_a_clone_failure_reports_and_exits_non_zero(self) -> None:
        absent = (self.sources / "PSMRI" / "Absent-Repo").as_uri()

        status = self.adhoc(absent)

        self.assertEqual(status, 1)
        self.assertFalse((self.workspace / "PSMRI" / "Absent-Repo").exists())

    def test_dry_run_creates_nothing(self) -> None:
        _, url = self.create_adhoc_source()

        status = self.adhoc(url, "--dry-run")

        self.assertEqual(status, 0)
        self.assertFalse(self.workspace.exists())

    def test_dry_run_reports_a_skip_for_an_existing_repository(self) -> None:
        _, url = self.create_adhoc_source()
        self.assertEqual(self.adhoc(url), 0)

        with contextlib.redirect_stdout(io.StringIO()) as captured:
            status = self.adhoc(url, "--dry-run")

        self.assertEqual(status, 0)
        self.assertIn("would skip", captured.getvalue())

    def test_dry_run_reports_a_failure_for_an_existing_non_git_path(self) -> None:
        _, url = self.create_adhoc_source()
        (self.workspace / "PSMRI" / "Some-New-Repo").mkdir(parents=True)

        with contextlib.redirect_stdout(io.StringIO()) as captured:
            status = self.adhoc(url, "--dry-run")

        self.assertEqual(status, 1)
        self.assertIn("would fail", captured.getvalue())

    def test_an_invalid_url_fails_before_anything_is_created(self) -> None:
        status = self.adhoc("not-a-url")

        self.assertEqual(status, 1)
        self.assertFalse(self.workspace.exists())

    def test_a_credential_bearing_url_fails_without_printing_the_secret(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            status = self.adhoc("https://user:s3cretvalue@github.com/PSMRI/Repo.git")

        self.assertEqual(status, 1)
        self.assertNotIn("s3cretvalue", buffer.getvalue())
        self.assertFalse(self.workspace.exists())

    def test_an_invalid_explicit_path_fails_before_anything_is_created(self) -> None:
        _, url = self.create_adhoc_source()

        status = self.adhoc(url, "--path", "../outside")

        self.assertEqual(status, 1)
        self.assertFalse(self.workspace.exists())

    def test_the_destination_always_stays_inside_the_workspace(self) -> None:
        _, url = self.create_adhoc_source()
        self.assertEqual(self.adhoc(url), 0)

        destination = (self.workspace / "PSMRI" / "Some-New-Repo").resolve()
        self.assertEqual(destination.parent.parent, self.workspace.resolve())

    def test_ad_hoc_cloning_works_in_a_workspace_path_containing_spaces(self) -> None:
        _, url = self.create_adhoc_source()
        workspace = self.root / "a workspace with spaces" / "repos"

        status = clone.main(
            ["--workspace", str(workspace), "--url", url]
        )

        self.assertEqual(status, 0)
        self.assertTrue(
            clone.is_git_repository(workspace / "PSMRI" / "Some-New-Repo")
        )


class AdHocModeExclusivityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.workspace = self.root / "repos"
        self.manifest = self.root / "manifest.txt"
        self.manifest.write_text(
            "PSMRI/Common-API|https://example.invalid/Common-API.git\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *arguments: str) -> int:
        return clone.main(
            [
                "--manifest",
                str(self.manifest),
                "--workspace",
                str(self.workspace),
                *arguments,
            ]
        )

    def test_a_selector_and_a_url_together_fail_before_cloning(self) -> None:
        status = self.run_cli(
            "Common-API", "--url", "https://github.com/PSMRI/Other.git"
        )
        self.assertEqual(status, 1)
        self.assertFalse(self.workspace.exists())

    def test_list_and_url_together_fail(self) -> None:
        status = self.run_cli("--list", "--url", "https://github.com/PSMRI/Other.git")
        self.assertEqual(status, 1)
        self.assertFalse(self.workspace.exists())

    def test_two_urls_fail(self) -> None:
        status = self.run_cli(
            "--url",
            "https://github.com/PSMRI/One.git",
            "--url",
            "https://github.com/PSMRI/Two.git",
        )
        self.assertEqual(status, 1)
        self.assertFalse(self.workspace.exists())

    def test_path_without_url_fails(self) -> None:
        status = self.run_cli("--path", "PSMRI/Some-Repo")
        self.assertEqual(status, 1)
        self.assertFalse(self.workspace.exists())

    def test_ad_hoc_mode_succeeds_even_when_the_manifest_is_absent(self) -> None:
        source_root = self.root / "sources"
        source_root.mkdir()
        source = create_source_repository(source_root / "PSMRI", "Some-New-Repo")

        status = clone.main(
            [
                "--manifest",
                str(self.root / "does-not-exist.txt"),
                "--workspace",
                str(self.workspace),
                "--url",
                source.as_uri(),
            ]
        )

        self.assertEqual(status, 0)
        self.assertTrue(
            clone.is_git_repository(self.workspace / "PSMRI" / "Some-New-Repo")
        )


class ManifestIsNeverAutoEditedTests(unittest.TestCase):
    """An ad-hoc clone is local workspace state, never a catalog change."""

    def test_ad_hoc_cloning_leaves_the_committed_manifest_byte_identical(self) -> None:
        before = MANIFEST_PATH.read_bytes()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = create_source_repository(root / "PSMRI", "Some-New-Repo")
            status = clone.main(
                [
                    "--workspace",
                    str(root / "repos"),
                    "--url",
                    source.as_uri(),
                ]
            )
            self.assertEqual(status, 0)

        self.assertEqual(MANIFEST_PATH.read_bytes(), before)

    def test_an_ad_hoc_repository_does_not_appear_in_list_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = root / "manifest.txt"
            manifest.write_text(
                "PSMRI/Common-API|https://example.invalid/Common-API.git\n",
                encoding="utf-8",
            )
            workspace = root / "repos"
            source = create_source_repository(root / "PSMRI", "Some-New-Repo")

            self.assertEqual(
                clone.main(
                    ["--workspace", str(workspace), "--url", source.as_uri()]
                ),
                0,
            )

            with contextlib.redirect_stdout(io.StringIO()) as captured:
                clone.main(
                    [
                        "--manifest",
                        str(manifest),
                        "--workspace",
                        str(workspace),
                        "--list",
                    ]
                )

            output = captured.getvalue()
            self.assertIn("PSMRI/Common-API", output)
            self.assertNotIn("Some-New-Repo", output)
            self.assertIn("Configured repositories: 1", output)


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
