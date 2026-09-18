"""Tests for scripts/update-skills.py.

Every test injects the release metadata, the release assets, and the
installation target. Nothing here performs a network call.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from zipfile import ZipFile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_TAG = "v1.4.3"
OLDER_TAG = "v1.4.2"


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


updater = load_script("test_update_skills", "update-skills.py")


def build_package(
    directory: Path,
    skill_name: str,
    root_name: str | None = None,
    include_manifest: bool = True,
    extra_entries: dict[str, str] | None = None,
    body: str = "Instructions.",
) -> Path:
    """Write a skill package ZIP shaped like scripts/package-skills.py output."""
    root_name = root_name or skill_name
    package = directory / f"{skill_name}.zip"
    with ZipFile(package, "w") as archive:
        if include_manifest:
            archive.writestr(
                f"{root_name}/SKILL.md",
                f"---\nname: {skill_name}\ndescription: Test skill.\n---\n\n{body}\n",
            )
            archive.writestr(f"{root_name}/references/guide.md", "Reference.\n")
        for name, content in (extra_entries or {}).items():
            archive.writestr(name, content)
    return package


def release_payload(tag: str, skill_names: list[str]) -> dict[str, object]:
    return {
        "tag_name": tag,
        "assets": [
            {
                "name": f"{name}.zip",
                "browser_download_url": f"https://example.invalid/{tag}/{name}.zip",
            }
            for name in skill_names
        ],
    }


class FakeGitHub:
    """An injected fetcher serving release metadata and asset bytes."""

    def __init__(self, tag: str, packages: dict[str, bytes]) -> None:
        self.tag = tag
        self.packages = packages
        self.payload = release_payload(tag, sorted(packages))
        self.requested: list[str] = []
        self.failures: dict[str, Exception] = {}

    def asset_url(self, name: str) -> str:
        return f"https://example.invalid/{self.tag}/{name}.zip"

    def __call__(self, url: str, accept: str = "*/*") -> bytes:
        self.requested.append(url)
        if url in self.failures:
            raise self.failures[url]
        if url.endswith(("/releases/latest", f"/tags/{self.tag}")):
            return json.dumps(self.payload).encode("utf-8")
        for name, payload in self.packages.items():
            if url == self.asset_url(name):
                return payload
        raise updater.UpdateError(f"unexpected URL {url}")


class UpdaterTestCase(unittest.TestCase):
    """Shared scaffolding: a fake home, a target, and a fake release."""

    skill_names = ["amrit-create-brd", "amrit-answer-codebase-questions"]

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.home = self.base / "home"
        self.skills_root = self.home / ".claude" / "skills"
        self.skills_root.mkdir(parents=True)
        self.build_directory = self.base / "packages"
        self.build_directory.mkdir()
        self.github = FakeGitHub(RELEASE_TAG, self.build_packages(self.skill_names))

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def build_packages(self, names: list[str]) -> dict[str, bytes]:
        return {
            name: build_package(self.build_directory, name).read_bytes()
            for name in names
        }

    def arguments(self, **overrides: object) -> argparse.Namespace:
        defaults = dict(
            skills=[],
            claude=False,
            agents=False,
            all_targets=False,
            target=None,
            check=False,
            dry_run=False,
            force=False,
            release=None,
            repository=updater.DEFAULT_REPOSITORY,
            list_skills=False,
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    def run_updater(self, **overrides: object) -> int:
        return updater.run(
            self.arguments(**overrides),
            REPOSITORY_ROOT,
            fetcher=self.github,
            home=self.home,
        )

    def release(self, tag: str = RELEASE_TAG) -> object:
        return updater.parse_release(release_payload(tag, sorted(self.github.packages)))

    def update(self, requested: list[str] | None = None, **overrides: object):
        return updater.update_target(
            self.release(),
            self.skills_root,
            requested or [],
            updater.DEFAULT_REPOSITORY,
            fetcher=self.github,
            **overrides,
        )

    def installed(self) -> list[str]:
        return updater.installed_skill_names(self.skills_root)

    def assert_installed(self, name: str) -> None:
        self.assertTrue((self.skills_root / name / "SKILL.md").is_file())


class SkillNameTests(unittest.TestCase):
    def test_keeps_an_already_prefixed_name(self) -> None:
        self.assertEqual(
            updater.normalize_skill_name("amrit-create-brd"), "amrit-create-brd"
        )

    def test_normalizes_unprefixed_shorthand(self) -> None:
        self.assertEqual(updater.normalize_skill_name("create-brd"), "amrit-create-brd")

    def test_never_double_prefixes(self) -> None:
        for raw in ("amrit-create-brd", "create-brd"):
            self.assertEqual(
                updater.normalize_skill_name(raw).count(updater.SKILL_PREFIX), 1
            )

    def test_accepts_a_package_filename(self) -> None:
        self.assertEqual(
            updater.normalize_skill_name("amrit-create-brd.zip"), "amrit-create-brd"
        )

    def test_rejects_an_empty_name(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "must not be empty"):
            updater.normalize_skill_name("  ")

    def test_rejects_a_malformed_name(self) -> None:
        for raw in ("Create_BRD", "amrit--create-brd", "../etc", "amrit-"):
            with self.subTest(raw=raw):
                with self.assertRaises(updater.UpdateError):
                    updater.normalize_skill_name(raw)

    def test_drops_duplicate_requests_and_keeps_order(self) -> None:
        self.assertEqual(
            updater.normalize_skill_names(["create-brd", "amrit-create-brd", "b-c"]),
            ["amrit-create-brd", "amrit-b-c"],
        )

    def test_only_amrit_packages_count_as_assets(self) -> None:
        self.assertEqual(asset := updater.asset_skill_name("amrit-create-brd.zip"), "amrit-create-brd")
        self.assertIsNotNone(asset)
        for other in ("bmad-build.zip", "create-brd.zip", "notes.txt", "amrit-create-brd.tar"):
            with self.subTest(other=other):
                self.assertIsNone(updater.asset_skill_name(other))


class ReleaseParsingTests(unittest.TestCase):
    def test_parses_only_amrit_skill_assets(self) -> None:
        payload = release_payload(RELEASE_TAG, ["amrit-create-brd"])
        payload["assets"].append(
            {"name": "checksums.txt", "browser_download_url": "https://example.invalid/x"}
        )
        release = updater.parse_release(payload)

        self.assertEqual(release.tag, RELEASE_TAG)
        self.assertEqual(release.skill_names(), ["amrit-create-brd"])

    def test_rejects_a_release_without_skill_packages(self) -> None:
        payload = {"tag_name": RELEASE_TAG, "assets": []}
        with self.assertRaisesRegex(updater.UpdateError, "carries no"):
            updater.parse_release(payload)

    def test_rejects_a_payload_without_a_tag(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "tag_name"):
            updater.parse_release({"assets": []})

    def test_rejects_a_tag_mismatch(self) -> None:
        payload = release_payload(OLDER_TAG, ["amrit-create-brd"])
        with self.assertRaisesRegex(updater.UpdateError, "but GitHub returned"):
            updater.parse_release(payload, expected_tag=RELEASE_TAG)

    def test_missing_release_asset_is_reported_with_the_available_skills(self) -> None:
        release = updater.parse_release(release_payload(RELEASE_TAG, ["amrit-create-brd"]))
        with self.assertRaises(updater.UpdateError) as raised:
            release.asset_url("amrit-not-published")

        message = str(raised.exception)
        self.assertIn("has no package for 'amrit-not-published'", message)
        self.assertIn("amrit-create-brd", message)

    def test_latest_and_tagged_api_urls(self) -> None:
        self.assertTrue(
            updater.release_api_url(updater.DEFAULT_REPOSITORY, None).endswith(
                "/releases/latest"
            )
        )
        self.assertTrue(
            updater.release_api_url(updater.DEFAULT_REPOSITORY, RELEASE_TAG).endswith(
                f"/releases/tags/{RELEASE_TAG}"
            )
        )

    def test_rejects_an_invalid_release_tag(self) -> None:
        for tag in ("1.0.3", "v1.0", "latest", "v1.0.3-rc1"):
            with self.subTest(tag=tag):
                with self.assertRaises(updater.UpdateError):
                    updater.validate_release_tag(tag)

    def test_rejects_an_invalid_repository(self) -> None:
        for repository in ("owner", "owner/name/extra", "../../etc"):
            with self.subTest(repository=repository):
                with self.assertRaises(updater.UpdateError):
                    updater.validate_repository(repository)

    def test_get_release_uses_the_injected_fetcher(self) -> None:
        github = FakeGitHub(RELEASE_TAG, {"amrit-create-brd": b""})
        release = updater.get_release(updater.DEFAULT_REPOSITORY, None, github)

        self.assertEqual(release.tag, RELEASE_TAG)
        self.assertTrue(github.requested[0].endswith("/releases/latest"))

    def test_get_release_reports_unparsable_metadata(self) -> None:
        def broken(url: str, accept: str = "*/*") -> bytes:
            return b"not json"

        with self.assertRaisesRegex(updater.UpdateError, "Could not parse"):
            updater.get_release(updater.DEFAULT_REPOSITORY, None, broken)


class ArchiveValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_accepts_a_well_formed_package(self) -> None:
        package = build_package(self.base, "amrit-create-brd")
        updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_malformed_zip(self) -> None:
        package = self.base / "amrit-create-brd.zip"
        package.write_bytes(b"this is not a zip archive")

        with self.assertRaisesRegex(updater.UpdateError, "not a valid ZIP"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_an_empty_zip(self) -> None:
        package = self.base / "amrit-create-brd.zip"
        with ZipFile(package, "w"):
            pass

        with self.assertRaisesRegex(updater.UpdateError, "empty"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_the_wrong_skill_root(self) -> None:
        package = build_package(self.base, "amrit-create-brd", root_name="create-brd")

        with self.assertRaisesRegex(updater.UpdateError, "outside the expected"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_root_belonging_to_another_skill(self) -> None:
        package = build_package(self.base, "amrit-create-brd", root_name="bmad-build")

        with self.assertRaisesRegex(updater.UpdateError, "outside the expected"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_traversal_entry(self) -> None:
        package = build_package(
            self.base,
            "amrit-create-brd",
            extra_entries={"amrit-create-brd/../../escaped.md": "pwned"},
        )

        with self.assertRaisesRegex(updater.UpdateError, "escapes the skill directory"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_an_absolute_entry(self) -> None:
        package = build_package(
            self.base, "amrit-create-brd", extra_entries={"/etc/passwd": "pwned"}
        )

        with self.assertRaisesRegex(updater.UpdateError, "absolute path"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_windows_absolute_entry(self) -> None:
        package = build_package(
            self.base, "amrit-create-brd", extra_entries={"C:/Windows/evil.md": "pwned"}
        )

        with self.assertRaises(updater.UpdateError):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_backslash_entry(self) -> None:
        # ZipFile.writestr normalizes backslashes to '/', so a hand-built
        # archive reaches the traversal guard first. Either rejection is
        # correct; what matters is that it never extracts.
        package = build_package(
            self.base,
            "amrit-create-brd",
            extra_entries={"amrit-create-brd\\..\\escaped.md": "pwned"},
        )

        with self.assertRaises(updater.UpdateError):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_literal_backslash_member_name(self) -> None:
        """An archive from another tool may store a real backslash."""
        with self.assertRaisesRegex(updater.UpdateError, "backslash"):
            updater.validate_archive_member(
                "amrit-create-brd\\..\\escaped.md", "amrit-create-brd"
            )

    def test_member_guard_accepts_a_well_formed_entry(self) -> None:
        updater.validate_archive_member(
            "amrit-create-brd/references/guide.md", "amrit-create-brd"
        )

    def test_rejects_a_package_without_a_manifest(self) -> None:
        package = build_package(
            self.base,
            "amrit-create-brd",
            include_manifest=False,
            extra_entries={"amrit-create-brd/README.md": "No manifest."},
        )

        with self.assertRaisesRegex(updater.UpdateError, "missing amrit-create-brd/SKILL.md"):
            updater.validate_archive(package, "amrit-create-brd")

    def test_rejects_a_symlink_entry(self) -> None:
        package = self.base / "amrit-create-brd.zip"
        with ZipFile(package, "w") as archive:
            archive.writestr("amrit-create-brd/SKILL.md", "---\nname: x\n---\n")
            info = updater.ZipInfo("amrit-create-brd/link")
            # 0xA1FF0000 sets S_IFLNK in the high bits of external_attr.
            info.external_attr = 0xA1FF0000
            archive.writestr(info, "/etc/passwd")

        with self.assertRaisesRegex(updater.UpdateError, "symbolic link"):
            updater.validate_archive(package, "amrit-create-brd")


class InstallationTargetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.home = self.base / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_claude_and_agent_targets_are_user_level(self) -> None:
        self.assertEqual(
            updater.target_root("claude", home=self.home),
            self.home / ".claude" / "skills",
        )
        self.assertEqual(
            updater.target_root("agents", home=self.home),
            self.home / ".agents" / "skills",
        )

    def test_rejects_an_unknown_target(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "Unknown target"):
            updater.target_root("vscode", home=self.home)

    def test_refuses_to_install_over_this_repositorys_claude_bridges(self) -> None:
        bridge_root = REPOSITORY_ROOT / ".claude" / "skills"

        with self.assertRaisesRegex(updater.UpdateError, "project bridge directory"):
            updater.resolve_skills_root(bridge_root, None, REPOSITORY_ROOT)

    def test_refuses_to_install_over_this_repositorys_agent_bridges(self) -> None:
        bridge_root = REPOSITORY_ROOT / ".agents" / "skills"

        with self.assertRaisesRegex(updater.UpdateError, "project bridge directory"):
            updater.resolve_skills_root(bridge_root, None, REPOSITORY_ROOT)

    def test_refuses_a_directory_inside_the_bridge_root(self) -> None:
        inside = REPOSITORY_ROOT / ".claude" / "skills" / "amrit-create-brd"

        with self.assertRaisesRegex(updater.UpdateError, "project bridge directory"):
            updater.resolve_skills_root(inside, None, REPOSITORY_ROOT)

    def test_accepts_an_explicit_directory_outside_the_repository(self) -> None:
        target = self.base / "other-project" / ".claude" / "skills"

        resolved = updater.resolve_skills_root(target, None, REPOSITORY_ROOT)

        self.assertEqual(resolved, target.resolve())

    def test_describes_a_user_level_target_portably(self) -> None:
        root = self.home / ".claude" / "skills"

        self.assertEqual(updater.describe_target(root, home=self.home), "~/.claude/skills")

    def test_target_cannot_be_combined_with_a_named_target(self) -> None:
        arguments = argparse.Namespace(
            target=Path("somewhere"), claude=True, agents=False, all_targets=False
        )

        with self.assertRaisesRegex(updater.UpdateError, "cannot be combined"):
            updater.selected_targets(arguments)

    def test_defaults_to_the_claude_target(self) -> None:
        arguments = argparse.Namespace(
            target=None, claude=False, agents=False, all_targets=False
        )

        self.assertEqual(updater.selected_targets(arguments), ["claude"])

    def test_all_selects_both_named_targets(self) -> None:
        arguments = argparse.Namespace(
            target=None, claude=False, agents=False, all_targets=True
        )

        self.assertEqual(updater.selected_targets(arguments), ["claude", "agents"])


class UpdateTests(UpdaterTestCase):
    def test_updates_every_amrit_skill_by_default(self) -> None:
        results = self.update()

        self.assertEqual(
            {result.status for result in results}, {updater.STATUS_UPDATED}
        )
        self.assertEqual(sorted(self.installed()), sorted(self.skill_names))
        for name in self.skill_names:
            self.assert_installed(name)

    def test_updates_only_the_requested_skill(self) -> None:
        results = self.update(["amrit-create-brd"])

        self.assertEqual([result.name for result in results], ["amrit-create-brd"])
        self.assertEqual(self.installed(), ["amrit-create-brd"])
        self.assertFalse((self.skills_root / "amrit-answer-codebase-questions").exists())

    def test_installs_the_full_skill_payload(self) -> None:
        self.update(["amrit-create-brd"])

        skill = self.skills_root / "amrit-create-brd"
        self.assertTrue((skill / "SKILL.md").is_file())
        self.assertTrue((skill / "references" / "guide.md").is_file())

    def test_unprefixed_shorthand_installs_the_prefixed_skill(self) -> None:
        requested = updater.normalize_skill_names(["create-brd"])

        self.update(requested)

        self.assertEqual(self.installed(), ["amrit-create-brd"])
        self.assertFalse((self.skills_root / "create-brd").exists())

    def test_leaves_unrelated_skills_untouched(self) -> None:
        for name in ("bmad-build", "my-own-skill", "gds-prd"):
            foreign = self.skills_root / name
            foreign.mkdir()
            (foreign / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")

        self.update()

        for name in ("bmad-build", "my-own-skill", "gds-prd"):
            with self.subTest(name=name):
                skill = self.skills_root / name
                self.assertTrue((skill / "SKILL.md").is_file())
                self.assertEqual(
                    (skill / "SKILL.md").read_text(encoding="utf-8"),
                    f"---\nname: {name}\n---\n",
                )

    def test_removes_stale_files_from_a_previous_installation(self) -> None:
        self.update(["amrit-create-brd"])
        stale = self.skills_root / "amrit-create-brd" / "references" / "removed.md"
        stale.write_text("Left over from an older release.\n", encoding="utf-8")

        self.update(["amrit-create-brd"], force=True)

        self.assertFalse(stale.exists())
        self.assert_installed("amrit-create-brd")

    def test_records_the_installed_release(self) -> None:
        self.update()

        state = updater.read_state(self.skills_root)
        self.assertEqual(state["release"], RELEASE_TAG)
        self.assertEqual(state["repository"], updater.DEFAULT_REPOSITORY)
        self.assertEqual(
            sorted(state["skills"]), sorted(self.skill_names)
        )
        self.assertEqual(state["skills"]["amrit-create-brd"], RELEASE_TAG)

    def test_state_file_is_not_mistaken_for_a_skill(self) -> None:
        self.update()

        self.assertTrue(updater.state_path(self.skills_root).is_file())
        self.assertNotIn(updater.STATE_FILENAME, self.installed())

    def test_second_run_reports_already_up_to_date(self) -> None:
        self.update()

        results = self.update()

        self.assertEqual({result.status for result in results}, {updater.STATUS_CURRENT})

    def test_force_reinstalls_a_current_skill(self) -> None:
        self.update()

        results = self.update(force=True)

        self.assertEqual({result.status for result in results}, {updater.STATUS_UPDATED})

    def test_reinstalls_when_the_recorded_release_is_older(self) -> None:
        self.update()
        updater.write_state(
            self.skills_root,
            updater.DEFAULT_REPOSITORY,
            OLDER_TAG,
            {name: OLDER_TAG for name in self.skill_names},
        )

        results = self.update()

        self.assertEqual({result.status for result in results}, {updater.STATUS_UPDATED})

    def test_reinstalls_when_the_directory_was_deleted_by_hand(self) -> None:
        self.update()
        updater.remove_tree(self.skills_root / "amrit-create-brd")

        results = self.update(["amrit-create-brd"])

        self.assertEqual([result.status for result in results], [updater.STATUS_UPDATED])
        self.assert_installed("amrit-create-brd")

    def test_dry_run_writes_nothing(self) -> None:
        results = self.update(dry_run=True)

        self.assertEqual({result.status for result in results}, {updater.STATUS_PLANNED})
        self.assertEqual(self.installed(), [])
        self.assertFalse(updater.state_path(self.skills_root).exists())

    def test_a_damaged_state_file_does_not_block_an_update(self) -> None:
        updater.state_path(self.skills_root).write_text("{ broken", encoding="utf-8")

        results = self.update()

        self.assertEqual({result.status for result in results}, {updater.STATUS_UPDATED})

    def test_creates_a_missing_target_directory(self) -> None:
        self.skills_root = self.home / ".agents" / "skills"

        self.update(["amrit-create-brd"])

        self.assert_installed("amrit-create-brd")


class FailureIsolationTests(UpdaterTestCase):
    def test_a_malformed_download_leaves_the_existing_skill_intact(self) -> None:
        self.update(["amrit-create-brd"])
        original = (self.skills_root / "amrit-create-brd" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.github.packages["amrit-create-brd"] = b"not a zip archive"

        results = self.update(["amrit-create-brd"], force=True)

        self.assertEqual([result.status for result in results], [updater.STATUS_FAILED])
        self.assertEqual(
            (self.skills_root / "amrit-create-brd" / "SKILL.md").read_text(
                encoding="utf-8"
            ),
            original,
        )

    def test_a_wrong_root_download_leaves_the_existing_skill_intact(self) -> None:
        self.update(["amrit-create-brd"])
        self.github.packages["amrit-create-brd"] = build_package(
            self.build_directory, "wrong", root_name="create-brd"
        ).read_bytes()

        results = self.update(["amrit-create-brd"], force=True)

        self.assertEqual([result.status for result in results], [updater.STATUS_FAILED])
        self.assert_installed("amrit-create-brd")

    def test_a_failed_download_leaves_the_existing_skill_intact(self) -> None:
        self.update(["amrit-create-brd"])
        self.github.failures[self.github.asset_url("amrit-create-brd")] = (
            updater.UpdateError("network is unreachable")
        )

        results = self.update(["amrit-create-brd"], force=True)

        self.assertEqual([result.status for result in results], [updater.STATUS_FAILED])
        self.assert_installed("amrit-create-brd")

    def test_one_failure_does_not_stop_the_other_skills(self) -> None:
        self.github.packages["amrit-create-brd"] = b"not a zip archive"

        results = self.update()

        statuses = {result.name: result.status for result in results}
        self.assertEqual(statuses["amrit-create-brd"], updater.STATUS_FAILED)
        self.assertEqual(
            statuses["amrit-answer-codebase-questions"], updater.STATUS_UPDATED
        )
        self.assert_installed("amrit-answer-codebase-questions")

    def test_a_failed_skill_is_not_recorded_as_installed(self) -> None:
        self.github.packages["amrit-create-brd"] = b"not a zip archive"

        self.update()

        recorded = updater.installed_releases(self.skills_root)
        self.assertNotIn("amrit-create-brd", recorded)
        self.assertIn("amrit-answer-codebase-questions", recorded)

    def test_no_staging_directories_are_left_behind(self) -> None:
        self.github.packages["amrit-create-brd"] = b"not a zip archive"

        self.update()

        leftovers = [
            path.name
            for path in self.skills_root.iterdir()
            if path.name.startswith(".") and path.name != updater.STATE_FILENAME
        ]
        self.assertEqual(leftovers, [])

    def test_install_refuses_a_non_amrit_destination(self) -> None:
        package = build_package(self.build_directory, "bmad-build")

        with self.assertRaisesRegex(updater.UpdateError, "unexpected directory"):
            updater.install_skill(package, "bmad-build", self.skills_root)

    def test_a_traversal_package_writes_nothing_outside_the_target(self) -> None:
        self.github.packages["amrit-create-brd"] = build_package(
            self.build_directory,
            "traversal",
            root_name="amrit-create-brd",
            extra_entries={"amrit-create-brd/../../escaped.md": "pwned"},
        ).read_bytes()

        results = self.update(["amrit-create-brd"])

        self.assertEqual([result.status for result in results], [updater.STATUS_FAILED])
        self.assertFalse((self.home / "escaped.md").exists())
        self.assertFalse((self.skills_root.parent / "escaped.md").exists())


class LongPathTests(UpdaterTestCase):
    """Windows rejects paths over 260 characters without the '\\\\?\\' form."""

    def test_strips_the_archive_root_component(self) -> None:
        relative = updater.member_relative_path(
            "amrit-create-brd/references/guide.md", "amrit-create-brd"
        )

        self.assertEqual(relative.as_posix(), "references/guide.md")

    def test_the_root_entry_itself_is_skipped(self) -> None:
        self.assertIsNone(
            updater.member_relative_path("amrit-create-brd/", "amrit-create-brd")
        )

    def test_long_path_is_unchanged_off_windows(self) -> None:
        if updater.os.name == "nt":
            self.skipTest("POSIX behaviour only")

        self.assertEqual(updater.long_path(Path("/tmp/x")), "/tmp/x")

    def test_long_path_uses_the_extended_form_on_windows(self) -> None:
        if updater.os.name != "nt":
            self.skipTest("Windows behaviour only")

        self.assertTrue(updater.long_path(self.skills_root).startswith("\\\\?\\"))

    def test_long_path_is_idempotent(self) -> None:
        once = updater.long_path(self.skills_root)

        self.assertEqual(updater.long_path(Path(once)), once)

    def test_installs_into_a_deeply_nested_target(self) -> None:
        """Regression: staging must not add the skill name to every path."""
        # Managed here rather than under the shared TemporaryDirectory:
        # tempfile's own cleanup uses plain paths and cannot delete a tree
        # this deep on Windows, whereas updater.remove_tree can.
        deep = Path(tempfile.mkdtemp())
        self.addCleanup(updater.remove_tree, deep)
        for _ in range(6):
            deep = deep / ("nested-directory-" + "x" * 20)
        skills_root = deep / ".claude" / "skills"
        self.assertGreater(len(str(skills_root)), 200)

        long_name = "references/" + "long-reference-file-name" * 2 + ".md"
        package = build_package(
            self.build_directory,
            "amrit-create-brd",
            extra_entries={f"amrit-create-brd/{long_name}": "Deep reference.\n"},
        )

        updater.install_skill(package, "amrit-create-brd", skills_root)

        # Asserted through long_path: the plain os/pathlib probes cannot see a
        # file this deep on Windows, which is the whole point of the helper.
        skill = skills_root / "amrit-create-brd"
        for relative in ("SKILL.md", long_name):
            with self.subTest(relative=relative):
                self.assertTrue(
                    updater.os.path.isfile(updater.long_path(skill / relative))
                )
        self.assertEqual(updater.installed_skill_names(skills_root), ["amrit-create-brd"])


class CheckTests(UpdaterTestCase):
    def test_check_reports_missing_skills_without_writing(self) -> None:
        results = updater.check_target(self.release(), self.skills_root, [])

        self.assertEqual({result.status for result in results}, {updater.STATUS_MISSING})
        self.assertEqual(self.installed(), [])
        self.assertFalse(updater.state_path(self.skills_root).exists())

    def test_check_reports_up_to_date_after_an_update(self) -> None:
        self.update()

        results = updater.check_target(self.release(), self.skills_root, [])

        self.assertEqual({result.status for result in results}, {updater.STATUS_CURRENT})

    def test_check_reports_a_behind_installation(self) -> None:
        self.update()
        updater.write_state(
            self.skills_root,
            updater.DEFAULT_REPOSITORY,
            OLDER_TAG,
            {name: OLDER_TAG for name in self.skill_names},
        )

        results = updater.check_target(self.release(), self.skills_root, [])

        self.assertEqual({result.status for result in results}, {updater.STATUS_BEHIND})
        self.assertTrue(all(result.detail == OLDER_TAG for result in results))

    def test_check_never_downloads_a_package(self) -> None:
        self.github.requested.clear()

        updater.check_target(self.release(), self.skills_root, [])

        self.assertEqual(self.github.requested, [])

    def test_check_of_one_skill_ignores_the_others(self) -> None:
        self.update(["amrit-create-brd"])

        results = updater.check_target(
            self.release(), self.skills_root, ["amrit-create-brd"]
        )

        self.assertEqual([result.status for result in results], [updater.STATUS_CURRENT])


class CommandLineTests(UpdaterTestCase):
    def test_default_run_updates_the_claude_target(self) -> None:
        self.assertEqual(self.run_updater(), 0)

        self.assertEqual(sorted(self.installed()), sorted(self.skill_names))

    def test_run_accepts_unprefixed_shorthand(self) -> None:
        self.assertEqual(self.run_updater(skills=["create-brd"]), 0)

        self.assertEqual(self.installed(), ["amrit-create-brd"])

    def test_run_with_all_updates_both_targets(self) -> None:
        self.assertEqual(self.run_updater(all_targets=True), 0)

        for relative in (".claude", ".agents"):
            root = self.home / relative / "skills"
            with self.subTest(target=relative):
                self.assertEqual(
                    sorted(updater.installed_skill_names(root)),
                    sorted(self.skill_names),
                )

    def test_run_with_an_explicit_target(self) -> None:
        target = self.base / "another-project" / ".claude" / "skills"

        self.assertEqual(self.run_updater(target=target), 0)

        self.assertEqual(
            sorted(updater.installed_skill_names(target)), sorted(self.skill_names)
        )

    def test_run_reports_a_failure_with_a_nonzero_exit_code(self) -> None:
        self.github.packages["amrit-create-brd"] = b"not a zip archive"

        self.assertEqual(self.run_updater(), 1)

    def test_run_rejects_check_combined_with_dry_run(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "cannot be combined"):
            self.run_updater(check=True, dry_run=True)

    def test_run_rejects_an_unknown_skill(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "has no package for"):
            self.run_updater(skills=["amrit-not-published"])

    def test_run_rejects_an_invalid_skill_name(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "Invalid skill name"):
            self.run_updater(skills=["Not A Skill"])

    def test_run_rejects_an_invalid_release_tag(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "Invalid release tag"):
            self.run_updater(release="latest")

    def test_run_rejects_an_invalid_repository(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "Invalid repository"):
            self.run_updater(repository="not-a-repository")

    def test_run_refuses_the_repository_bridge_directory(self) -> None:
        with self.assertRaisesRegex(updater.UpdateError, "project bridge directory"):
            self.run_updater(target=REPOSITORY_ROOT / ".claude" / "skills")

    def test_check_run_writes_nothing(self) -> None:
        self.assertEqual(self.run_updater(check=True), 0)

        self.assertEqual(self.installed(), [])

    def test_list_run_writes_nothing(self) -> None:
        self.assertEqual(self.run_updater(list_skills=True), 0)

        self.assertEqual(self.installed(), [])

    def test_run_accepts_a_pinned_release(self) -> None:
        self.assertEqual(self.run_updater(release=RELEASE_TAG), 0)

        self.assertEqual(sorted(self.installed()), sorted(self.skill_names))

    def test_parser_accepts_the_documented_invocations(self) -> None:
        parser = updater.build_parser()

        for argv in (
            [],
            ["amrit-create-brd"],
            ["create-brd", "amrit-answer-codebase-questions"],
            ["--claude"],
            ["--agents"],
            ["--all"],
            ["--check"],
            ["--dry-run"],
            ["--force"],
            ["--list"],
            ["--release", "v1.0.3"],
            ["--target", "./.claude/skills"],
        ):
            with self.subTest(argv=argv):
                parser.parse_args(argv)


class ShippedSkillIntegrationTests(unittest.TestCase):
    """The updater must agree with what this repository actually publishes."""

    def canonical_skill_names(self) -> list[str]:
        return sorted(
            path.name
            for path in (REPOSITORY_ROOT / "skills").iterdir()
            if path.is_dir()
        )

    def test_every_canonical_skill_is_an_amrit_skill(self) -> None:
        for name in self.canonical_skill_names():
            with self.subTest(name=name):
                self.assertRegex(name, updater.SKILL_NAME_PATTERN)

    def test_every_canonical_skill_maps_to_a_recognised_release_asset(self) -> None:
        for name in self.canonical_skill_names():
            with self.subTest(name=name):
                self.assertEqual(updater.asset_skill_name(f"{name}.zip"), name)

    def test_every_canonical_skill_survives_name_normalization(self) -> None:
        for name in self.canonical_skill_names():
            with self.subTest(name=name):
                self.assertEqual(updater.normalize_skill_name(name), name)

    def test_shorthand_resolves_to_every_canonical_skill(self) -> None:
        for name in self.canonical_skill_names():
            shorthand = name[len(updater.SKILL_PREFIX) :]
            with self.subTest(shorthand=shorthand):
                self.assertEqual(updater.normalize_skill_name(shorthand), name)

    def test_the_default_repository_is_the_framework_repository(self) -> None:
        self.assertEqual(updater.DEFAULT_REPOSITORY, "PSMRI/AMRIT-AI-Agentic-Framework")


if __name__ == "__main__":
    unittest.main()
