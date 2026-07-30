from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from zipfile import ZipFile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, filename: str) -> ModuleType:
    script_path = REPOSITORY_ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


packaging = load_script("test_package_skills", "package-skills.py")
validation = load_script("test_validate_skills", "validate-skills.py")


def create_skill(repo_root: Path, name: str, body: str = "Instructions.") -> Path:
    skill_directory = repo_root / "skills" / name
    skill_directory.mkdir(parents=True)
    (skill_directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill.\n---\n\n{body}\n",
        encoding="utf-8",
    )
    return skill_directory


def create_bridge(repo_root: Path, name: str, target_name: str | None = None) -> Path:
    target_name = target_name or name
    bridge_directory = repo_root / ".claude" / "skills" / name
    bridge_directory.mkdir(parents=True)
    bridge = bridge_directory / "SKILL.md"
    bridge.write_text(
        "---\n"
        f"name: {name}\n"
        "description: Test project bridge.\n"
        "---\n\n"
        f"[Canonical skill](../../../skills/{target_name}/SKILL.md)\n",
        encoding="utf-8",
    )
    return bridge


class PackagingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_packages_one_valid_skill_with_correct_root(self) -> None:
        skill_directory = create_skill(self.repo_root, "sample-skill")
        (skill_directory / "references").mkdir()
        (skill_directory / "references" / "guide.md").write_text(
            "Guide", encoding="utf-8"
        )

        package = packaging.package_skill(self.repo_root, "sample-skill")

        with ZipFile(package) as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    "sample-skill/SKILL.md",
                    "sample-skill/references/guide.md",
                ],
            )
            self.assertTrue(
                all(name.startswith("sample-skill/") for name in archive.namelist())
            )

    def test_packages_all_valid_skills(self) -> None:
        create_skill(self.repo_root, "alpha-skill")
        create_skill(self.repo_root, "beta-skill")

        packages = packaging.package_all(self.repo_root)

        self.assertEqual(
            [path.name for path in packages],
            ["alpha-skill.zip", "beta-skill.zip"],
        )
        self.assertTrue(all(path.is_file() for path in packages))

    def test_unknown_skill_fails(self) -> None:
        create_skill(self.repo_root, "known-skill")

        with self.assertRaisesRegex(packaging.PackagingError, "Unknown skill"):
            packaging.package_skill(self.repo_root, "unknown-skill")

    def test_missing_skill_manifest_fails(self) -> None:
        (self.repo_root / "skills" / "broken-skill").mkdir(parents=True)

        with self.assertRaisesRegex(packaging.PackagingError, "missing"):
            packaging.package_skill(self.repo_root, "broken-skill")

    def test_excludes_temporary_generated_and_repository_files(self) -> None:
        skill_directory = create_skill(self.repo_root, "filtered-skill")
        excluded_files = [
            skill_directory / "__pycache__" / "cache.pyc",
            skill_directory / ".pytest_cache" / "state",
            skill_directory / ".git" / "config",
            skill_directory / ".github" / "workflow.yml",
            skill_directory / ".claude" / "settings.json",
            skill_directory / "dist" / "old.zip",
            skill_directory / "scratch.tmp",
            skill_directory / "backup.bak",
            skill_directory / "generated.zip",
            skill_directory / "editor-file~",
        ]
        for path in excluded_files:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("excluded", encoding="utf-8")
        (skill_directory / "keep.txt").write_text("included", encoding="utf-8")

        package = packaging.package_skill(self.repo_root, "filtered-skill")

        with ZipFile(package) as archive:
            names = archive.namelist()
        self.assertIn("filtered-skill/keep.txt", names)
        self.assertEqual(
            names,
            ["filtered-skill/SKILL.md", "filtered-skill/keep.txt"],
        )

    def test_recreates_an_existing_zip(self) -> None:
        skill_directory = create_skill(self.repo_root, "replaceable-skill", "Version 1")
        package = packaging.package_skill(self.repo_root, "replaceable-skill")
        package.write_bytes(b"stale and invalid")
        (skill_directory / "SKILL.md").write_text(
            "---\n"
            "name: replaceable-skill\n"
            "description: Test skill.\n"
            "---\n\n"
            "Version 2\n",
            encoding="utf-8",
        )

        recreated = packaging.package_skill(self.repo_root, "replaceable-skill")

        with ZipFile(recreated) as archive:
            manifest = archive.read("replaceable-skill/SKILL.md").decode("utf-8")
        self.assertIn("Version 2", manifest)

    def test_archive_is_deterministic(self) -> None:
        create_skill(self.repo_root, "stable-skill")

        first = packaging.package_skill(self.repo_root, "stable-skill").read_bytes()
        second = packaging.package_skill(self.repo_root, "stable-skill").read_bytes()

        self.assertEqual(first, second)


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_accepts_project_bridge_and_resolves_target(self) -> None:
        skill = create_skill(self.repo_root, "mapped-skill")
        create_bridge(self.repo_root, "mapped-skill")

        errors = validation.validate_project_mappings(self.repo_root, [skill])
        self.assertEqual(errors, [])

    def test_rejects_mapping_to_wrong_source(self) -> None:
        skill = create_skill(self.repo_root, "mapped-skill")
        create_skill(self.repo_root, "other-skill")
        create_bridge(self.repo_root, "mapped-skill", "other-skill")

        errors = validation.validate_project_mappings(self.repo_root, [skill])

        self.assertEqual(len(errors), 1)
        self.assertIn("must reference canonical skill", errors[0])


if __name__ == "__main__":
    unittest.main()
