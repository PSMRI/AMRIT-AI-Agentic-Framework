from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from zipfile import BadZipFile, ZipFile


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_packaging_module() -> ModuleType:
    script_path = Path(__file__).resolve().with_name("package-skills.py")
    spec = importlib.util.spec_from_file_location("amrit_package_skills", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load packaging script: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discover_skills(repo_root: Path) -> tuple[list[Path], list[str]]:
    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        return [], [f"Missing skills directory: {skills_root}"]

    try:
        skills = sorted(
            (path for path in skills_root.iterdir() if path.is_dir()),
            key=lambda path: path.name,
        )
    except OSError as error:
        return [], [f"Could not read {skills_root}: {error}"]

    if not skills:
        return [], [f"No skill directories found in {skills_root}"]
    return skills, []


def validate_manifests(skills: list[Path]) -> list[str]:
    errors: list[str] = []
    for skill in skills:
        manifest = skill / "SKILL.md"
        if not manifest.is_file():
            errors.append(f"{skill}: missing SKILL.md")
    return errors


def validate_project_mappings(repo_root: Path, skills: list[Path]) -> list[str]:
    errors: list[str] = []
    mappings_root = repo_root / ".claude" / "skills"
    if not mappings_root.is_dir():
        return [f"Missing project skills directory: {mappings_root}"]

    expected_names = {skill.name for skill in skills}
    try:
        actual_names = {path.name for path in mappings_root.iterdir()}
    except OSError as error:
        return [f"Could not read {mappings_root}: {error}"]

    for skill in skills:
        bridge = mappings_root / skill.name / "SKILL.md"
        if not bridge.is_file():
            errors.append(f"{bridge}: missing project skill bridge")
            continue

        expected_relative = Path("..") / ".." / ".." / "skills" / skill.name / "SKILL.md"
        expected_link = expected_relative.as_posix()
        try:
            bridge_text = bridge.read_text(encoding="utf-8")
            resolved_target = (bridge.parent / expected_relative).resolve(strict=True)
            canonical_target = (skill / "SKILL.md").resolve(strict=True)
        except (OSError, UnicodeError) as error:
            errors.append(f"{bridge}: could not resolve canonical skill: {error}")
            continue

        if expected_link not in bridge_text:
            errors.append(
                f"{bridge}: must reference canonical skill {expected_link}"
            )
        if resolved_target != canonical_target:
            errors.append(
                f"{bridge}: resolves to {resolved_target}, expected {canonical_target}"
            )

    for extra_name in sorted(actual_names - expected_names):
        errors.append(
            f"{mappings_root / extra_name}: has no matching source skill"
        )
    return errors


def validate_zip_structure(package: Path, skill_name: str) -> list[str]:
    try:
        with ZipFile(package) as archive:
            names = archive.namelist()
    except (OSError, BadZipFile) as error:
        return [f"{package}: unreadable ZIP: {error}"]

    if not names:
        return [f"{package}: ZIP is empty"]

    expected_prefix = f"{skill_name}/"
    errors: list[str] = []
    if any(not name.startswith(expected_prefix) for name in names):
        errors.append(
            f"{package}: every archive path must start with {expected_prefix}"
        )
    if f"{skill_name}/SKILL.md" not in names:
        errors.append(f"{package}: missing {skill_name}/SKILL.md")
    return errors


def validate_packaging(repo_root: Path, skills: list[Path]) -> list[str]:
    try:
        packaging = load_packaging_module()
    except (OSError, RuntimeError) as error:
        return [f"Could not load packaging logic: {error}"]

    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="amrit-skill-validation-") as temporary:
        output_directory = Path(temporary)
        for skill in skills:
            try:
                package = packaging.package_skill(
                    repo_root, skill.name, output_directory
                )
            except Exception as error:
                errors.append(f"Packaging '{skill.name}' failed: {error}")
                continue
            errors.extend(validate_zip_structure(package, skill.name))
    return errors


def validate_tracked_zips(repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", "*.zip"],
            cwd=repo_root,
            check=False,
            capture_output=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    tracked = [
        value.decode("utf-8", errors="replace")
        for value in result.stdout.split(b"\0")
        if value
        and (repo_root / value.decode("utf-8", errors="replace")).exists()
    ]
    return (
        ["Generated ZIP files are tracked by Git: " + ", ".join(tracked)]
        if tracked
        else []
    )


def validate_repository(repo_root: Path) -> tuple[list[str], list[str]]:
    repo_root = repo_root.resolve()
    skills, errors = discover_skills(repo_root)
    errors.extend(validate_manifests(skills))
    errors.extend(validate_project_mappings(repo_root, skills))
    errors.extend(validate_packaging(repo_root, skills))
    errors.extend(validate_tracked_zips(repo_root))
    return [skill.name for skill in skills], errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AMRIT release and project-discovery invariants."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=get_repo_root(),
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    skill_names, errors = validate_repository(args.repo_root)
    if errors:
        print(f"Skill validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_names)} skill(s): {', '.join(skill_names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
