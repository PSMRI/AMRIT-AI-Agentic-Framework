"""Clone the configured AMRIT application repositories into the local workspace.

The workspace directory is ignored by the AMRIT AI Agentic Framework
repository. Every repository cloned beneath it stays a fully independent Git
repository with its own remote, branches, and history.

The script is safe to run repeatedly. An existing repository is reported and
left exactly as the developer left it: it is never re-cloned, reset, cleaned,
checked out, or pulled.

Two modes, never combined:

* manifest mode, the default, clones repositories configured in
  config/amrit-repositories.txt, optionally narrowed by selectors;
* ad-hoc mode, --url, clones one repository that is not in the manifest. It
  neither reads nor writes the manifest, and the clone is local workspace
  state only.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


DEFAULT_MANIFEST = Path("config") / "amrit-repositories.txt"
DEFAULT_WORKSPACE = Path("repos")

# A workspace path segment: no separators, no traversal, no percent-encoding,
# and never leading with '-' so it can never be mistaken for a command flag.
WORKSPACE_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9._-]*$")

# SSH "scp" syntax, for example git@github.com:PSMRI/Some-Repo.git
SCP_URL_PATTERN = re.compile(
    r"^(?P<user>[A-Za-z0-9._-]+@)?(?P<host>[A-Za-z0-9._-]+):(?P<path>(?!/).*)$"
)

URL_SCHEMES = frozenset({"https", "http", "ssh", "git", "file"})

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


class AdHocRepositoryError(Exception):
    """Raised when an ad-hoc --url or --path cannot be used safely."""


@dataclass(frozen=True)
class RepositoryEntry:
    """One repository to clone: its workspace path and its clone URL.

    Manifest-backed and ad-hoc repositories share this type, so both travel
    through exactly the same cloning and reporting code.
    """

    path: str
    url: str
    line_number: int = 0

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


def validate_segment(segment: str, role: str) -> str:
    """Validate one workspace path segment, rejecting anything unsafe."""

    if not segment:
        raise AdHocRepositoryError(f"the {role} is empty")
    if segment in {".", ".."}:
        raise AdHocRepositoryError(f"the {role} must not be '{segment}'")
    if "\\" in segment or "/" in segment:
        raise AdHocRepositoryError(f"the {role} must not contain a path separator")
    if "%" in segment:
        raise AdHocRepositoryError(
            f"the {role} must not contain percent-encoded characters"
        )
    if not WORKSPACE_SEGMENT_PATTERN.match(segment):
        raise AdHocRepositoryError(
            f"the {role} '{segment}' is not a valid directory name; use letters, "
            "digits, '.', '_', or '-'"
        )
    return segment


def split_workspace_path(text: str) -> tuple[str, str]:
    """Validate an explicit '<organization>/<repository>' workspace path."""

    candidate = text.strip()
    if not candidate:
        raise AdHocRepositoryError("the workspace path is empty")
    if "\\" in candidate:
        raise AdHocRepositoryError(
            "the workspace path must use '/' as its only separator"
        )
    if candidate.startswith("/"):
        raise AdHocRepositoryError(
            "the workspace path must be relative to the workspace directory"
        )
    if Path(candidate).is_absolute():
        raise AdHocRepositoryError(
            "the workspace path must be relative to the workspace directory"
        )

    segments = candidate.split("/")
    if len(segments) != 2:
        raise AdHocRepositoryError(
            "the workspace path must be exactly '<organization>/<repository>', "
            f"got: {text}"
        )
    organization = validate_segment(segments[0], "organization")
    repository = validate_segment(segments[1], "repository name")
    return organization, repository


def reject_credentials(url: str) -> None:
    """Refuse a URL carrying inline credentials, without ever echoing them.

    Runs before any other parsing, so no later message can quote a secret.
    """

    remainder = url
    scheme = ""
    if "://" in remainder:
        scheme, remainder = remainder.split("://", 1)
        scheme = scheme.lower()
    authority = remainder.split("/", 1)[0]

    if "@" not in authority:
        return

    userinfo = authority.rsplit("@", 1)[0]
    if ":" in userinfo:
        raise AdHocRepositoryError(
            "the clone URL contains inline credentials; remove them and "
            "configure Git authentication instead"
        )
    if scheme in {"http", "https"}:
        raise AdHocRepositoryError(
            "the clone URL contains an inline user or token; remove it and "
            "configure Git authentication instead"
        )


def parse_clone_url(url: str) -> tuple[str, str]:
    """Derive '<organization>', '<repository>' from a clone URL.

    Supports HTTPS-style URLs and SSH 'scp' syntax. Never guesses: a URL that
    does not clearly carry both an organization and a repository is rejected.
    """

    candidate = url.strip()
    if not candidate:
        raise AdHocRepositoryError("the clone URL is empty")
    if any(character.isspace() for character in candidate):
        raise AdHocRepositoryError("the clone URL must not contain whitespace")

    # Always first, so no later error message can quote a credential.
    reject_credentials(candidate)

    scp_match = SCP_URL_PATTERN.match(candidate)
    if scp_match and "://" not in candidate:
        path = scp_match.group("path")
    else:
        parsed = urlsplit(candidate)
        if not parsed.scheme:
            raise AdHocRepositoryError(
                "the clone URL has no scheme; use an https:// URL such as "
                "https://github.com/<organization>/<repository>.git"
            )
        if parsed.scheme.lower() not in URL_SCHEMES:
            raise AdHocRepositoryError(
                f"unsupported clone URL scheme '{parsed.scheme}'; use one of: "
                + ", ".join(sorted(URL_SCHEMES))
            )
        path = parsed.path

    if "\\" in path:
        raise AdHocRepositoryError(
            "the clone URL path must use '/' as its only separator"
        )

    segments = [segment for segment in path.split("/") if segment]
    if any(segment in {".", ".."} for segment in segments):
        raise AdHocRepositoryError(
            "the clone URL path must not contain '.' or '..' segments"
        )
    if segments and segments[-1].endswith(".git"):
        segments[-1] = segments[-1][: -len(".git")]
        segments = [segment for segment in segments if segment]

    if len(segments) < 2:
        raise AdHocRepositoryError(
            "the clone URL does not identify both an organization and a "
            f"repository: {candidate}"
        )

    organization = validate_segment(segments[-2], "organization")
    repository = validate_segment(segments[-1], "repository name")
    return organization, repository


def build_adhoc_entry(url: str, explicit_path: str | None) -> RepositoryEntry:
    """Build a RepositoryEntry for an ad-hoc clone, validating its path."""

    if explicit_path is not None:
        organization, repository = split_workspace_path(explicit_path)
        # Still validate the URL itself, including its credential rules.
        parse_clone_url(url)
    else:
        organization, repository = parse_clone_url(url)
    return RepositoryEntry(path=f"{organization}/{repository}", url=url.strip())


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
        "--url",
        action="append",
        default=None,
        metavar="CLONE_URL",
        help=(
            "Ad-hoc mode: clone one repository that is not in the manifest, "
            "for example https://github.com/PSMRI/Some-New-Repo.git. The "
            "destination is derived from the URL unless --path is given. The "
            "manifest is neither read nor modified. Cannot be combined with "
            "repository selectors or --list, and may be given only once."
        ),
    )
    parser.add_argument(
        "--path",
        default=None,
        metavar="ORG/REPO",
        help=(
            "Advanced override for --url: the destination beneath the "
            "workspace, which must be exactly '<organization>/<repository>'"
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


def check_mode(arguments: argparse.Namespace) -> str:
    """Resolve the invocation to exactly one mode, or explain the conflict."""

    urls = arguments.url or []
    if urls:
        if arguments.repositories:
            raise AdHocRepositoryError(
                "repository selectors and --url are separate modes; pass "
                "either manifest selectors or one --url, not both"
            )
        if arguments.list:
            raise AdHocRepositoryError(
                "--list reports manifest state and cannot be combined with --url"
            )
        if len(urls) > 1:
            raise AdHocRepositoryError(
                "only one --url may be given per invocation; run the script "
                "once per ad-hoc repository"
            )
        return "adhoc"

    if arguments.path is not None:
        raise AdHocRepositoryError("--path is only meaningful together with --url")
    return "manifest"


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    repo_root = get_repo_root()

    manifest = resolve_argument_path(arguments.manifest, repo_root / DEFAULT_MANIFEST)
    workspace = resolve_argument_path(
        arguments.workspace, repo_root / DEFAULT_WORKSPACE
    )

    try:
        mode = check_mode(arguments)
    except AdHocRepositoryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if mode == "adhoc":
        # Ad-hoc mode never opens the manifest, so it can never mutate it.
        try:
            selected = [build_adhoc_entry(arguments.url[0], arguments.path)]
        except AdHocRepositoryError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        source_line = "Source:    ad-hoc --url; the manifest is not read or changed"
    else:
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
                    f"{display_path(manifest, repo_root)}. To clone a "
                    "repository that is not in the manifest, pass its clone "
                    "URL with --url.",
                    file=sys.stderr,
                )
            return 1

        if arguments.list:
            return report_status(selected, workspace, repo_root)

        source_line = f"Manifest:  {display_path(manifest, repo_root)}"

    if not arguments.dry_run:
        try:
            workspace.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            print(f"error: could not create {workspace}: {error}", file=sys.stderr)
            return 1

    print(source_line)
    print(f"Workspace: {display_path(workspace, repo_root)}")
    print(f"Repositories to process: {len(selected)}")
    if mode == "adhoc":
        destination = destination_for(selected[0], workspace)
        print(f"Destination: {display_path(destination, repo_root)}")
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
