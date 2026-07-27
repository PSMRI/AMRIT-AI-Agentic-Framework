from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def package_skill(skill_name: str) -> Path:
    repo_root = Path(__file__).resolve().parent.parent
    skill_directory = repo_root / "skills" / skill_name
    output_directory = repo_root / "skill-zips"
    output_file = output_directory / f"{skill_name}.zip"

    if not skill_directory.is_dir():
        raise FileNotFoundError(
            f"Skill directory does not exist: {skill_directory}"
        )

    output_directory.mkdir(parents=True, exist_ok=True)

    with ZipFile(output_file, "w", ZIP_DEFLATED) as archive:
        for file_path in sorted(skill_directory.rglob("*")):
            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(skill_directory)

            # ZIP files must use forward slashes internally.
            archive_path = (Path(skill_name) / relative_path).as_posix()

            archive.write(file_path, archive_path)

    print(f"Created skill package: {output_file}")
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package an AMRIT SDLC skill as a portable ZIP."
    )
    parser.add_argument(
        "skill_name",
        help="Folder name inside the skills directory.",
    )
    args = parser.parse_args()

    package_skill(args.skill_name)


if __name__ == "__main__":
    main()