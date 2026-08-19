"""Clone the configured AMRIT application repositories into the local workspace.

The workspace directory is ignored by the AMRIT AI Agentic Framework
repository. Every repository cloned beneath it stays a fully independent Git
repository with its own remote, branches, and history.

The script is safe to run repeatedly. An existing repository is reported and
left exactly as the developer left it: it is never re-cloned, reset, cleaned,
checked out, or pulled.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MANIFEST = Path("config") / "amrit-repositories.txt"
DEFAULT_WORKSPACE = Path("repos")

STATUS_CLONED = "cloned"
STATUS_PRESENT = "present"
STATUS_FAILED = "failed"
STATUS_PLANNED = "planned"

STATUS_MARKERS = {
    STATUS_CLONED: "OK  ",
    STATUS_PRESENT: "SKIP",
    STATUS_PLANNED: "PLAN",
    STATUS_FAILED: "FAIL",
}


class ManifestError(Exception):
    """Raised when the repository manifest cannot be used as configured."""


@dataclass(frozen=True)
class RepositoryEntry:
    """One configured repository: its workspace path and its clone URL."""

    path: str
    url: str
    line_number: int

    @property
    def organization(self) -> str:
        return self.path.split("/")[0]

    @property
    def name(self) -> str:
        return self.path.split("/")[1]


@dataclass
class RepositoryResult:
    entry: RepositoryEntry
    status: str
    detail: str


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_manifest(text: str) -> list[RepositoryEntry]:
    """Parse manifest text into entries, rejecting malformed configuration."""

    entries: list[RepositoryEntry] = []
    seen: dict[str, int] = {}

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.count("|") != 1:
            raise ManifestError(
                f"Line {line_number}: expected "
                f"'<organization>/<repository>|<clone-url>', got: {line}"
            )

        raw_path, raw_url = (field.strip() for field in line.split("|"))
        path = raw_path.strip("/").replace("\\", "/")
        url = raw_url

        if not path or not url:
            raise ManifestError(
                f"Line {line_number}: both a repository path and a clone URL "
                "are required"
            )

        segments = [segment for segment in path.split("/") if segment]
        if len(segments) != 2:
            raise ManifestError(
                f"Line {line_number}: repository path must be "
                f"'<organization>/<repository>', got: {raw_path}"
            )
        if any(segment in {".", ".."} for segment in segments):
            raise ManifestError(
                f"Line {line_number}: repository path must not contain '.' or '..'"
            )

        path = "/".join(segments)
        if path in seen:
            raise ManifestError(
                f"Line {line_number}: duplicate repository path '{path}' "
                f"(already configured on line {seen[path]})"
            )
        seen[path] = line_number
        entries.append(RepositoryEntry(path=path, url=url, line_number=line_number))

    if not entries:
        raise ManifestError("No repositories are configured in the manifest")
    return entries


def read_manifest(manifest: Path) -> list[RepositoryEntry]:
    try:
        text = manifest.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ManifestError(f"Repository manifest not found: {manifest}") from error
    except OSError as error:
        raise ManifestError(f"Could not read {manifest}: {error}") from error
    return parse_manifest(text)


def select_entries(
    entries: list[RepositoryEntry], selectors: list[str]
) -> tuple[list[RepositoryEntry], list[str]]:
    """Filter entries by repository name or '<organization>/<repository>'."""

    if not selectors:
        return entries, []

    selected: list[RepositoryEntry] = []
    unmatched: list[str] = []
    for selector in selectors:
        wanted = selector.strip().strip("/").replace("\\", "/").lower()
        matches = [
            entry
            for entry in entries
            if entry.path.lower() == wanted or entry.name.lower() == wanted
        ]
        if not matches:
            unmatched.append(selector)
            continue
        for match in matches:
            if match not in selected:
                selected.append(match)
    return selected, unmatched


def run_git(
    arguments: list[str], cwd: Path | None = None, capture: bool = False
) -> subprocess.CompletedProcess[str] | None:
    """Run a git command, returning None when git itself cannot be executed."""

    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=str(cwd) if cwd is not None else None,
            check=False,
            text=True,
            capture_output=capture,
        )
    except (OSError, subprocess.SubprocessError):
        return None


def is_git_repository(path: Path) -> bool:
    """Report whether path is the top level of a usable Git repository."""

    if not (path / ".git").exists():
        return False
    completed = run_git(["rev-parse", "--is-inside-work-tree"], cwd=path, capture=True)
    return completed is not None and completed.returncode == 0


def describe_existing(path: Path) -> str:
    completed = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path, capture=True)
    if completed is not None and completed.returncode == 0:
        branch = completed.stdout.strip()
        if branch:
            return f"already present (on {branch}); left untouched"
    return "already present; left untouched"


def clone_repository(entry: RepositoryEntry, destination: Path) -> RepositoryResult:
    """Clone one repository, never touching an existing path."""

    if destination.exists():
        if is_git_repository(destination):
            return RepositoryResult(
                entry, STATUS_PRESENT, describe_existing(destination)
            )
        return RepositoryResult(
            entry,
            STATUS_FAILED,
            "path exists but is not a Git repository; nothing was changed. "
            "Move or remove it manually, then re-run.",
        )

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        return RepositoryResult(
            entry, STATUS_FAILED, f"could not create {destination.parent}: {error}"
        )

    completed = run_git(["clone", entry.url, str(destination)])
    if completed is None:
        return RepositoryResult(
            entry, STATUS_FAILED, "git could not be executed; is Git installed?"
        )
    if completed.returncode != 0:
        return RepositoryResult(
            entry,
            STATUS_FAILED,
            f"git clone exited with status {completed.returncode}; check network "
            "access, repository access rights, and Git authentication",
        )
    return RepositoryResult(entry, STATUS_CLONED, "cloned")


def workspace_status(destination: Path) -> str:
    if not destination.exists():
        return "missing"
    if is_git_repository(destination):
        return "cloned"
    return "invalid"


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root)).replace(os.sep, "/")
    except ValueError:
        return str(path)


def destination_for(entry: RepositoryEntry, workspace: Path) -> Path:
    return workspace / entry.organization / entry.name


def report_status(
    entries: list[RepositoryEntry], workspace: Path, repo_root: Path
) -> int:
    print(f"Workspace: {display_path(workspace, repo_root)}")
    print(f"Configured repositories: {len(entries)}")
    print("")

    counts = {"cloned": 0, "missing": 0, "invalid": 0}
    for entry in entries:
        status = workspace_status(destination_for(entry, workspace))
        counts[status] += 1
        print(f"  [{status:>7}] {entry.path}")

    print("")
    print(
        f"Summary: {counts['cloned']} cloned, {counts['missing']} missing, "
        f"{counts['invalid']} invalid"
    )
    if counts["invalid"]:
        print(
            "An 'invalid' path exists in the workspace but is not a Git "
            "repository. Resolve it manually; this script never deletes "
            "workspace content."
        )
        return 1
    return 0


def clone_all(
    entries: list[RepositoryEntry], workspace: Path, dry_run: bool = False
) -> list[RepositoryResult]:
    """Process every entry, continuing past individual failures."""

    results: list[RepositoryResult] = []
    for entry in entries:
        destination = destination_for(entry, workspace)
        if dry_run:
            status = workspace_status(destination)
            if status == "cloned":
                result = RepositoryResult(
                    entry, STATUS_PRESENT, "already present; would skip"
                )
            elif status == "invalid":
                result = RepositoryResult(
                    entry,
                    STATUS_FAILED,
                    "path exists but is not a Git repository; would fail",
                )
            else:
                result = RepositoryResult(
                    entry, STATUS_PLANNED, f"would clone from {entry.url}"
                )
        else:
            result = clone_repository(entry, destination)

        results.append(result)
        print(f"  [{STATUS_MARKERS[result.status]}] {entry.path}: {result.detail}")
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Clone the configured AMRIT application repositories into the "
            "local, Git-ignored workspace directory."
        )
    )
    parser.add_argument(
        "repositories",
        nargs="*",
        help=(
            "Optional repository selectors, given as 'Common-API' or "
            "'PSMRI/Common-API'. Every configured repository is used when "
            "omitted."
        ),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help=f"Repository manifest to read (default: {DEFAULT_MANIFEST.as_posix()})",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help=(
            "Workspace directory to clone into "
            f"(default: {DEFAULT_WORKSPACE.as_posix()}/)"
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help=(
            "Report configured, cloned, missing, and invalid repositories, "
            "then exit"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the actions that would be taken without cloning anything",
    )
    return parser


def resolve_argument_path(candidate: Path | None, fallback: Path) -> Path:
    if candidate is None:
        return fallback
    if candidate.is_absolute():
        return candidate
    return (Path.cwd() / candidate).resolve()


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    repo_root = get_repo_root()

    manifest = resolve_argument_path(arguments.manifest, repo_root / DEFAULT_MANIFEST)
    workspace = resolve_argument_path(
        arguments.workspace, repo_root / DEFAULT_WORKSPACE
    )

    try:
        entries = read_manifest(manifest)
    except ManifestError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    selected, unmatched = select_entries(entries, arguments.repositories)
    if unmatched:
        for selector in unmatched:
            print(
                f"error: '{selector}' is not configured in "
                f"{display_path(manifest, repo_root)}",
                file=sys.stderr,
            )
        return 1

    if arguments.list:
        return report_status(selected, workspace, repo_root)

    if not arguments.dry_run:
        try:
            workspace.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            print(f"error: could not create {workspace}: {error}", file=sys.stderr)
            return 1

    print(f"Manifest:  {display_path(manifest, repo_root)}")
    print(f"Workspace: {display_path(workspace, repo_root)}")
    print(f"Repositories to process: {len(selected)}")
    print("")

    results = clone_all(selected, workspace, dry_run=arguments.dry_run)

    cloned = [result for result in results if result.status == STATUS_CLONED]
    present = [result for result in results if result.status == STATUS_PRESENT]
    planned = [result for result in results if result.status == STATUS_PLANNED]
    failed = [result for result in results if result.status == STATUS_FAILED]

    print("")
    print("Summary")
    print(f"  cloned:          {len(cloned)}")
    print(f"  already present: {len(present)}")
    if planned:
        print(f"  would clone:     {len(planned)}")
    print(f"  failed:          {len(failed)}")

    if present:
        print("")
        print(
            "Existing repositories were left untouched. Fetch or pull from "
            "inside the repository itself when you want to update it:"
        )
        example = destination_for(present[0].entry, workspace)
        print(f"  cd {display_path(example, repo_root)} && git pull")

    if failed:
        print("")
        print("Failed repositories:")
        for result in failed:
            print(f"  {result.entry.path}: {result.detail}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
