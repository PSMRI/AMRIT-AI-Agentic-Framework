from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_install_directory(scope: str, project_path: str | None) -> Path:
    if scope == "user":
        return Path.home() / ".claude" / "skills"

    project_directory = (
        Path(project_path).expanduser().resolve()
        if project_path
        else Path.cwd().resolve()
    )
    return project_directory / ".claude" / "skills"


def get_available_skills(skills_directory: Path) -> list[str]:
    if not skills_directory.is_dir():
        return []

    return sorted(
        directory.name
        for directory in skills_directory.iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    )


def validate_skill(skills_directory: Path, skill_name: str) -> Path:
    source_directory = skills_directory / skill_name

    if not source_directory.is_dir() or not (source_directory / "SKILL.md").is_file():
        available = get_available_skills(skills_directory)
        available_text = ", ".join(available) or "none"
        raise FileNotFoundError(
            f"Unknown or invalid skill: {skill_name}\n"
            f"Available skills: {available_text}"
        )

    return source_directory


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def install_skill(
    skills_directory: Path,
    install_directory: Path,
    skill_name: str,
    replace_existing: bool,
) -> tuple[Path, str]:
    source_directory = validate_skill(skills_directory, skill_name)
    destination_directory = install_directory / skill_name
    install_directory.mkdir(parents=True, exist_ok=True)

    action = "Installed"
    if destination_directory.exists() or destination_directory.is_symlink():
        if not replace_existing:
            raise FileExistsError(
                f"Skill is already installed at:\n"
                f"  {destination_directory}\n\n"
                f"Run with --upgrade to replace it."
            )
        remove_path(destination_directory)
        action = "Upgraded"

    shutil.copytree(source_directory, destination_directory)
    return destination_directory, action


def uninstall_skill(install_directory: Path, skill_name: str) -> Path:
    destination_directory = install_directory / skill_name

    if not destination_directory.exists() and not destination_directory.is_symlink():
        raise FileNotFoundError(
            f"Skill is not installed at:\n  {destination_directory}"
        )

    remove_path(destination_directory)
    return destination_directory


def print_available_skills(skills_directory: Path, install_directory: Path) -> None:
    skills = get_available_skills(skills_directory)

    if not skills:
        print("No valid skills were found in the repository.")
        return

    print("Available skills:\n")
    for skill_name in skills:
        destination = install_directory / skill_name
        status = "installed" if destination.exists() or destination.is_symlink() else "not installed"
        print(f"  - {skill_name} ({status})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install AMRIT SDLC skills into Claude Code."
    )

    parser.add_argument(
        "skill_name",
        nargs="?",
        help="Name of one skill folder inside skills/.",
    )
    parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help=(
            "Installation scope: 'user' installs into ~/.claude/skills; "
            "'project' installs into <project>/.claude/skills."
        ),
    )
    parser.add_argument(
        "--project-path",
        help=(
            "Target project directory for --scope project. "
            "Defaults to the current working directory."
        ),
    )

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--list",
        action="store_true",
        help="List repository skills and show whether each is installed.",
    )
    action_group.add_argument(
        "--all",
        action="store_true",
        help="Install every valid skill in the repository.",
    )
    action_group.add_argument(
        "--uninstall",
        metavar="SKILL_NAME",
        help="Uninstall one skill from the selected scope.",
    )

    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Replace an already-installed skill with the repository version.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Backward-compatible alias for --upgrade.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.project_path and args.scope != "project":
        parser.error("--project-path can only be used with --scope project")

    if args.upgrade and args.uninstall:
        parser.error("--upgrade cannot be combined with --uninstall")

    if args.skill_name and (args.list or args.all or args.uninstall):
        parser.error(
            "Do not provide a positional skill name with --list, --all, or --uninstall"
        )

    if not args.skill_name and not (args.list or args.all or args.uninstall):
        parser.error("provide a skill name, --list, --all, or --uninstall SKILL_NAME")

    repo_root = get_repo_root()
    skills_directory = repo_root / "skills"
    install_directory = get_install_directory(args.scope, args.project_path)
    replace_existing = args.upgrade or args.force

    try:
        if args.list:
            print_available_skills(skills_directory, install_directory)
            return

        if args.uninstall:
            removed_path = uninstall_skill(install_directory, args.uninstall)
            print(f"Uninstalled Claude Code skill: {args.uninstall}")
            print(f"Removed: {removed_path}")
            return

        if args.all:
            skill_names = get_available_skills(skills_directory)
            if not skill_names:
                raise FileNotFoundError("No valid skills were found in the repository.")

            installed_count = 0
            skipped: list[str] = []

            for skill_name in skill_names:
                try:
                    destination, action = install_skill(
                        skills_directory,
                        install_directory,
                        skill_name,
                        replace_existing,
                    )
                    print(f"{action}: {skill_name} -> {destination}")
                    installed_count += 1
                except FileExistsError:
                    skipped.append(skill_name)

            print(f"\nCompleted: {installed_count} skill(s) installed or upgraded.")
            if skipped:
                print("Skipped already-installed skills: " + ", ".join(skipped))
                print("Run again with --upgrade to replace them.")
            return

        destination, action = install_skill(
            skills_directory,
            install_directory,
            args.skill_name,
            replace_existing,
        )
        print(f"{action} Claude Code skill: {args.skill_name}")
        print(f"Location: {destination}")

    except (FileNotFoundError, FileExistsError, PermissionError, OSError) as error:
        print(f"Operation failed:\n{error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()