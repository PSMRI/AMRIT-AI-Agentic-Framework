from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


RELEASE_VERSION_FILENAME = ".release-version"
RELEASE_LINE_PATTERN = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


class ReleaseVersionError(RuntimeError):
    """Raised when the next release version cannot be determined safely."""


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_release_line(raw_release_line: str) -> tuple[int, int]:
    """Parse the manually controlled MAJOR.MINOR release line.

    The release line never contains a patch number; Git tags are the only
    source of truth for the patch component.
    """
    release_line = raw_release_line.strip()
    if not release_line:
        raise ReleaseVersionError(
            f"{RELEASE_VERSION_FILENAME} is empty. It must contain exactly one "
            "MAJOR.MINOR release line, for example '1.0'."
        )

    match = RELEASE_LINE_PATTERN.fullmatch(release_line)
    if match is None:
        raise ReleaseVersionError(
            f"{RELEASE_VERSION_FILENAME} contains {release_line!r}, which is not a "
            "MAJOR.MINOR release line. Use two non-negative integers with no "
            "leading 'v', no patch number, and no suffix, for example '1.0', "
            "'2.4', or '10.12'."
        )
    return int(match.group(1)), int(match.group(2))


def read_release_line(release_version_file: Path) -> tuple[int, int]:
    try:
        contents = release_version_file.read_text(encoding="utf-8")
    except OSError as error:
        raise ReleaseVersionError(
            f"Could not read {release_version_file}: {error}"
        ) from error
    except UnicodeError as error:
        raise ReleaseVersionError(
            f"{release_version_file} is not valid UTF-8: {error}"
        ) from error
    return parse_release_line(contents)


def build_release_tag_pattern(major: int, minor: int) -> re.Pattern[str]:
    """Match only 'vMAJOR.MINOR.PATCH' tags on the configured release line."""
    return re.compile(rf"^v{major}\.{minor}\.(0|[1-9][0-9]*)$")


def select_release_patches(major: int, minor: int, tags: Iterable[str]) -> list[int]:
    """Return the sorted, numerically compared patch numbers already released.

    Tags on other release lines, prerelease-like tags, and any tag that does
    not match the exact pattern are ignored.
    """
    pattern = build_release_tag_pattern(major, minor)
    patches: set[int] = set()
    for tag in tags:
        match = pattern.fullmatch(tag.strip())
        if match is not None:
            patches.add(int(match.group(1)))
    return sorted(patches)


def calculate_next_patch(major: int, minor: int, tags: Iterable[str]) -> int:
    """The next patch is one above the highest released patch, or 0 if none."""
    patches = select_release_patches(major, minor, tags)
    return patches[-1] + 1 if patches else 0


def calculate_next_tag(raw_release_line: str, tags: Iterable[str]) -> str:
    major, minor = parse_release_line(raw_release_line)
    return f"v{major}.{minor}.{calculate_next_patch(major, minor, tags)}"


def split_tags(raw_tags: str) -> list[str]:
    return [line.strip() for line in raw_tags.splitlines() if line.strip()]


def read_tags_from_file(tags_file: Path) -> list[str]:
    if str(tags_file) == "-":
        return split_tags(sys.stdin.read())
    try:
        return split_tags(tags_file.read_text(encoding="utf-8"))
    except OSError as error:
        raise ReleaseVersionError(f"Could not read {tags_file}: {error}") from error
    except UnicodeError as error:
        raise ReleaseVersionError(
            f"{tags_file} is not valid UTF-8: {error}"
        ) from error


def read_tags_from_git(repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "tag", "--list"],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise ReleaseVersionError(f"Could not run git: {error}") from error

    if result.returncode != 0:
        detail = result.stderr.strip() or "git tag --list failed"
        raise ReleaseVersionError(f"Could not list Git tags: {detail}")
    return split_tags(result.stdout)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Print the next 'vMAJOR.MINOR.PATCH' release tag for the release "
            "line configured in .release-version. MAJOR.MINOR is maintained by "
            "hand; PATCH is derived from existing Git tags."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=get_repo_root(),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--release-version-file",
        type=Path,
        default=None,
        help=f"Path to the release-line file. Defaults to {RELEASE_VERSION_FILENAME}.",
    )
    parser.add_argument(
        "--tags-file",
        type=Path,
        default=None,
        help=(
            "Read candidate tags, one per line, from this file. Use '-' for "
            "standard input. Defaults to 'git tag --list' in the repository."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = args.repo_root.resolve()
    release_version_file = (
        args.release_version_file
        if args.release_version_file is not None
        else repo_root / RELEASE_VERSION_FILENAME
    )

    try:
        major, minor = read_release_line(release_version_file)
        tags = (
            read_tags_from_file(args.tags_file)
            if args.tags_file is not None
            else read_tags_from_git(repo_root)
        )
        next_patch = calculate_next_patch(major, minor, tags)
    except ReleaseVersionError as error:
        print(f"Release version calculation failed: {error}", file=sys.stderr)
        return 1

    print(f"v{major}.{minor}.{next_patch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
