from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile, ZipInfo


SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXCLUDED_DIRECTORY_NAMES = {
    ".agents",
    ".claude",
    ".git",
    ".github",
    ".pytest_cache",
    "__pycache__",
    "dist",
}
EXCLUDED_FILE_NAMES = {".DS_Store", "Desktop.ini", "Thumbs.db"}
EXCLUDED_FILE_SUFFIXES = {".bak", ".pyc", ".pyo", ".temp", ".tmp", ".zip"}
DETERMINISTIC_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class PackagingError(RuntimeError):
    """Raised when a skill cannot be packaged safely."""


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_directory = repo_root / "skills"
    if not skills_directory.is_dir():
        raise PackagingError(f"Skills directory does not exist: {skills_directory}")

    try:
        names = sorted(
            path.name for path in skills_directory.iterdir() if path.is_dir()
        )
    except OSError as error:
        raise PackagingError(
            f"Could not read skills directory {skills_directory}: {error}"
        ) from error

    if not names:
        raise PackagingError(f"No skill directories found in {skills_directory}")
    return names


def validate_skill_source(repo_root: Path, skill_name: str) -> Path:
    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        raise PackagingError(
            f"Invalid skill name '{skill_name}'. "
            "Use lowercase letters, numbers, and single hyphens."
        )

    skill_directory = repo_root / "skills" / skill_name
    if not skill_directory.is_dir():
        available = ", ".join(discover_skill_names(repo_root))
        raise PackagingError(
            f"Unknown skill '{skill_name}'. Available skills: {available}"
        )

    manifest = skill_directory / "SKILL.md"
    if not manifest.is_file():
        raise PackagingError(f"Skill '{skill_name}' is missing {manifest}")
    try:
        if not manifest.read_bytes().strip():
            raise PackagingError(f"Skill '{skill_name}' has an empty {manifest}")
    except OSError as error:
        raise PackagingError(f"Could not read {manifest}: {error}") from error

    return skill_directory


def should_exclude(relative_path: Path) -> bool:
    if any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_path.parts):
        return True

    name = relative_path.name
    return (
        name in EXCLUDED_FILE_NAMES
        or name.endswith("~")
        or relative_path.suffix.lower() in EXCLUDED_FILE_SUFFIXES
    )


def collect_skill_files(skill_directory: Path) -> list[Path]:
    files: list[Path] = []
    try:
        candidates = sorted(
            skill_directory.rglob("*"),
            key=lambda path: path.relative_to(skill_directory).as_posix(),
        )
    except OSError as error:
        raise PackagingError(
            f"Could not enumerate files in {skill_directory}: {error}"
        ) from error

    for path in candidates:
        relative_path = path.relative_to(skill_directory)
        if should_exclude(relative_path):
            continue
        if path.is_symlink():
            raise PackagingError(
                f"Skill source contains a symbolic link, which is not packaged: {path}"
            )
        if path.is_file():
            files.append(path)

    if not files:
        raise PackagingError(f"Skill contains no packageable files: {skill_directory}")
    return files


def build_zip(
    skill_name: str,
    skill_directory: Path,
    files: list[Path],
    output_file: Path,
) -> None:
    try:
        with ZipFile(
            output_file,
            "w",
            compression=ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            for file_path in files:
                relative_path = file_path.relative_to(skill_directory)
                archive_path = (Path(skill_name) / relative_path).as_posix()
                try:
                    contents = file_path.read_bytes()
                except OSError as error:
                    raise PackagingError(
                        f"Could not read required file {file_path}: {error}"
                    ) from error

                info = ZipInfo(archive_path, date_time=DETERMINISTIC_TIMESTAMP)
                info.compress_type = ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (0o100644 & 0xFFFF) << 16
                archive.writestr(info, contents, compress_type=ZIP_DEFLATED, compresslevel=9)
    except (OSError, BadZipFile) as error:
        raise PackagingError(
            f"Could not create package for '{skill_name}': {error}"
        ) from error


def package_skill(
    repo_root: Path,
    skill_name: str,
    output_directory: Path | None = None,
) -> Path:
    repo_root = repo_root.resolve()
    skill_directory = validate_skill_source(repo_root, skill_name)
    files = collect_skill_files(skill_directory)
    destination_directory = (
        output_directory.resolve()
        if output_directory is not None
        else repo_root / "dist"
    )

    try:
        destination_directory.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise PackagingError(
            f"Could not create output directory {destination_directory}: {error}"
        ) from error

    output_file = destination_directory / f"{skill_name}.zip"
    temporary_path: Path | None = None
    try:
        descriptor, raw_temporary_path = tempfile.mkstemp(
            prefix=f".{skill_name}-",
            suffix=".zip.tmp",
            dir=destination_directory,
        )
        os.close(descriptor)
        temporary_path = Path(raw_temporary_path)
        build_zip(skill_name, skill_directory, files, temporary_path)
        temporary_path.replace(output_file)
    except PackagingError:
        raise
    except OSError as error:
        raise PackagingError(
            f"Could not safely replace package {output_file}: {error}"
        ) from error
    finally:
        if temporary_path is not None and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                pass

    return output_file


def package_all(repo_root: Path, output_directory: Path | None = None) -> list[Path]:
    return [
        package_skill(repo_root, skill_name, output_directory)
        for skill_name in discover_skill_names(repo_root)
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Package AMRIT skills as deterministic installable ZIP files."
    )
    parser.add_argument(
        "skill_name",
        nargs="?",
        help="Name of one skill directory under skills/.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Package every skill directory under skills/.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.all == bool(args.skill_name):
        parser.error("provide exactly one skill name or --all")

    repo_root = get_repo_root()
    try:
        packages = (
            package_all(repo_root)
            if args.all
            else [package_skill(repo_root, args.skill_name)]
        )
    except PackagingError as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        return 1

    for package in packages:
        print(f"Created {package.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
