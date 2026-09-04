"""Update the locally installed AMRIT skills from the latest GitHub Release.

This is an explicit command a developer runs. Nothing here polls, schedules,
or updates anything in the background.

The update source is always a published GitHub Release of this framework, whose
assets are the individual per-skill ZIP packages produced by
scripts/package-skills.py. Raw files from a branch are never an update source.

Only directories named 'amrit-*' are ever created, replaced, or removed in an
installation target. Skills belonging to other frameworks, and skills the
developer wrote themselves, are left untouched.

The repository's own .claude/skills/ and .agents/skills/ directories hold small
project bridges that point at the canonical skills under skills/. They are a
Git-tracked part of the framework, not an installation target, so this script
refuses to write into them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable, Sequence
from zipfile import BadZipFile, ZipFile, ZipInfo


DEFAULT_REPOSITORY = "PSMRI/AMRIT-AI-Agentic-Framework"
SKILL_PREFIX = "amrit-"
STATE_FILENAME = ".amrit-skills.json"
PACKAGE_SUFFIX = ".zip"
MANIFEST_KEY = "SKILL.md"
USER_AGENT = "amrit-update-skills"
GITHUB_API = "https://api.github.com"
API_MEDIA_TYPE = "application/vnd.github+json"
TOKEN_VARIABLES = ("AMRIT_GITHUB_TOKEN", "GITHUB_TOKEN", "GH_TOKEN")
MAXIMUM_PACKAGE_BYTES = 64 * 1024 * 1024

# 'amrit-' followed by lowercase, hyphen-separated words: the exact shape
# scripts/package-skills.py accepts, narrowed to the AMRIT namespace.
SKILL_NAME_PATTERN = re.compile(r"^amrit-[a-z0-9]+(?:-[a-z0-9]+)*$")
RELEASE_TAG_PATTERN = re.compile(r"^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")

TARGET_CLAUDE = "claude"
TARGET_AGENTS = "agents"
TARGET_ROOTS = {
    TARGET_CLAUDE: Path(".claude") / "skills",
    TARGET_AGENTS: Path(".agents") / "skills",
}

STATUS_UPDATED = "updated"
STATUS_CURRENT = "current"
STATUS_PLANNED = "planned"
STATUS_BEHIND = "behind"
STATUS_MISSING = "missing"
STATUS_FAILED = "failed"

STATUS_MARKERS = {
    STATUS_UPDATED: "OK  ",
    STATUS_CURRENT: "SKIP",
    STATUS_PLANNED: "PLAN",
    STATUS_BEHIND: "OLD ",
    STATUS_MISSING: "NEW ",
    STATUS_FAILED: "FAIL",
}


class UpdateError(RuntimeError):
    """Raised when the installed skills cannot be updated safely."""


@dataclass(frozen=True)
class Release:
    """A published release and the skill packages attached to it."""

    tag: str
    assets: dict[str, str] = field(default_factory=dict)

    def skill_names(self) -> list[str]:
        return sorted(self.assets)

    def asset_url(self, skill_name: str) -> str:
        try:
            return self.assets[skill_name]
        except KeyError:
            available = ", ".join(self.skill_names()) or "none"
            raise UpdateError(
                f"Release {self.tag} has no package for '{skill_name}'. "
                f"Skills published in {self.tag}: {available}"
            ) from None


@dataclass(frozen=True)
class SkillResult:
    """The outcome of one skill in one installation target."""

    name: str
    status: str
    detail: str = ""

    @classmethod
    def failure(cls, name: str, message: str) -> "SkillResult":
        """Record a failure, without repeating the skill name in the detail."""
        prefix = f"{name}: "
        while message.startswith(prefix):
            message = message[len(prefix) :]
        return cls(name, STATUS_FAILED, message)


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------
# Skill names
# --------------------------------------------------------------------------


def normalize_skill_name(raw_name: str) -> str:
    """Accept 'create-brd' as shorthand for the real name 'amrit-create-brd'.

    The shorthand is an input convenience only. The old unprefixed name is
    never a real skill name, and is never installed or exposed.
    """
    name = raw_name.strip()
    if not name:
        raise UpdateError("A skill name must not be empty")
    if name.endswith(PACKAGE_SUFFIX):
        name = name[: -len(PACKAGE_SUFFIX)]
    if not name.startswith(SKILL_PREFIX):
        name = f"{SKILL_PREFIX}{name}"
    if not SKILL_NAME_PATTERN.fullmatch(name):
        raise UpdateError(
            f"Invalid skill name {raw_name!r}. Use lowercase, hyphen-separated "
            f"words, for example 'amrit-create-brd' or the shorthand 'create-brd'"
        )
    return name


def normalize_skill_names(raw_names: Iterable[str]) -> list[str]:
    """Normalize every requested name, preserving order and dropping repeats."""
    selected: list[str] = []
    for raw_name in raw_names:
        name = normalize_skill_name(raw_name)
        if name not in selected:
            selected.append(name)
    return selected


def asset_skill_name(asset_name: str) -> str | None:
    """The skill an asset filename belongs to, or None if it is not one."""
    if not asset_name.endswith(PACKAGE_SUFFIX):
        return None
    name = asset_name[: -len(PACKAGE_SUFFIX)]
    return name if SKILL_NAME_PATTERN.fullmatch(name) else None


# --------------------------------------------------------------------------
# Release discovery
# --------------------------------------------------------------------------


def github_token() -> str | None:
    """An optional token. The public repository does not require one."""
    for variable in TOKEN_VARIABLES:
        token = os.environ.get(variable, "").strip()
        if token:
            return token
    return None


def build_request(url: str, accept: str) -> urllib.request.Request:
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def describe_http_error(error: urllib.error.HTTPError, url: str) -> str:
    """Turn an HTTP failure into something a developer can act on."""
    remaining = error.headers.get("X-RateLimit-Remaining") if error.headers else None
    if error.code in (403, 429) and remaining == "0":
        hint = (
            "set GITHUB_TOKEN to a personal access token to raise the limit"
            if github_token() is None
            else "wait for the rate-limit window to reset"
        )
        reset = error.headers.get("X-RateLimit-Reset") if error.headers else None
        when = ""
        if reset and reset.isdigit():
            moment = datetime.fromtimestamp(int(reset), tz=timezone.utc)
            when = f" (resets at {moment.isoformat(timespec='seconds')})"
        return f"GitHub API rate limit exceeded{when}; {hint}"
    if error.code == 404:
        return (
            f"Not found: {url}. The repository may be private, or it may have "
            "no published release yet"
        )
    if error.code == 401:
        return (
            f"Unauthorized: {url}. A token is set but was rejected; unset it to "
            "use anonymous access to a public repository"
        )
    return f"HTTP {error.code} {error.reason} for {url}"


def fetch_bytes(url: str, accept: str = "*/*") -> bytes:
    """Read a URL with the standard library. No third-party dependency."""
    try:
        with urllib.request.urlopen(build_request(url, accept)) as response:
            return response.read(MAXIMUM_PACKAGE_BYTES + 1)
    except urllib.error.HTTPError as error:
        raise UpdateError(describe_http_error(error, url)) from error
    except urllib.error.URLError as error:
        raise UpdateError(f"Could not reach {url}: {error.reason}") from error
    except OSError as error:
        raise UpdateError(f"Could not read {url}: {error}") from error


Fetcher = Callable[[str, str], bytes]


def default_fetcher(url: str, accept: str = "*/*") -> bytes:
    return fetch_bytes(url, accept)


def parse_release(payload: object, expected_tag: str | None = None) -> Release:
    """Build a Release from a GitHub release API payload."""
    if not isinstance(payload, dict):
        raise UpdateError("The GitHub release response was not a JSON object")

    tag = payload.get("tag_name")
    if not isinstance(tag, str) or not tag.strip():
        raise UpdateError("The GitHub release response has no 'tag_name'")
    tag = tag.strip()
    if expected_tag is not None and tag != expected_tag:
        raise UpdateError(
            f"Requested release {expected_tag} but GitHub returned {tag}"
        )

    raw_assets = payload.get("assets")
    if not isinstance(raw_assets, list):
        raise UpdateError(f"Release {tag} has no asset list")

    assets: dict[str, str] = {}
    for entry in raw_assets:
        if not isinstance(entry, dict):
            continue
        asset_name = entry.get("name")
        url = entry.get("browser_download_url")
        if not isinstance(asset_name, str) or not isinstance(url, str):
            continue
        skill_name = asset_skill_name(asset_name)
        if skill_name is None:
            continue
        assets[skill_name] = url

    if not assets:
        raise UpdateError(
            f"Release {tag} carries no {SKILL_PREFIX}*{PACKAGE_SUFFIX} skill "
            "packages. Install from a release published by the Release Skills "
            "workflow"
        )
    return Release(tag=tag, assets=assets)


def release_api_url(repository: str, tag: str | None) -> str:
    validate_repository(repository)
    if tag is None:
        return f"{GITHUB_API}/repos/{repository}/releases/latest"
    return f"{GITHUB_API}/repos/{repository}/releases/tags/{tag}"


def validate_repository(repository: str) -> str:
    if not REPOSITORY_PATTERN.fullmatch(repository):
        raise UpdateError(
            f"Invalid repository {repository!r}. Use '<owner>/<name>', for "
            f"example {DEFAULT_REPOSITORY}"
        )
    return repository


def validate_release_tag(tag: str) -> str:
    if not RELEASE_TAG_PATTERN.fullmatch(tag):
        raise UpdateError(
            f"Invalid release tag {tag!r}. Releases of this framework are "
            "tagged 'vMAJOR.MINOR.PATCH', for example 'v1.0.3'"
        )
    return tag


def get_release(
    repository: str = DEFAULT_REPOSITORY,
    tag: str | None = None,
    fetcher: Fetcher = default_fetcher,
) -> Release:
    """Resolve the latest release, or one specific tag."""
    if tag is not None:
        validate_release_tag(tag)
    url = release_api_url(repository, tag)
    raw = fetcher(url, API_MEDIA_TYPE)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise UpdateError(f"Could not parse the release response from {url}: {error}")
    return parse_release(payload, expected_tag=tag)


# --------------------------------------------------------------------------
# Installation targets
# --------------------------------------------------------------------------


def target_root(target: str, home: Path | None = None) -> Path:
    """The user-level skills directory for a supported target."""
    if target not in TARGET_ROOTS:
        supported = ", ".join(sorted(TARGET_ROOTS))
        raise UpdateError(f"Unknown target {target!r}. Supported targets: {supported}")
    base = home if home is not None else Path.home()
    return base / TARGET_ROOTS[target]


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def reject_repository_bridges(skills_root: Path, repo_root: Path) -> None:
    """Never install packages over this repository's project bridges.

    .claude/skills/ and .agents/skills/ in this checkout hold Git-tracked
    bridge files that scripts/validate-skills.py verifies. Replacing one with a
    full skill package would corrupt the framework's own source tree.
    """
    for relative in TARGET_ROOTS.values():
        bridge_root = (repo_root / relative).resolve()
        if skills_root == bridge_root or is_inside(skills_root, bridge_root):
            raise UpdateError(
                f"{skills_root} is this repository's project bridge directory, "
                "not an installation target. In a framework clone the skills are "
                "already available through the bridges; update them with "
                "'git pull'. To install packaged skills, target a skills "
                "directory outside this repository"
            )


def resolve_skills_root(
    explicit: Path | None,
    target: str | None,
    repo_root: Path,
    home: Path | None = None,
) -> Path:
    """Where skills will be installed, after every safety check."""
    if explicit is not None:
        root = Path(explicit).expanduser()
        if not root.is_absolute():
            root = (Path.cwd() / root).resolve()
        else:
            root = root.resolve()
    else:
        if target is None:
            raise UpdateError("No installation target was selected")
        root = target_root(target, home=home).resolve()

    reject_repository_bridges(root, repo_root)
    return root


def describe_target(skills_root: Path, home: Path | None = None) -> str:
    """A short, portable label for a skills root."""
    base = (home if home is not None else Path.home()).resolve()
    try:
        return f"~/{skills_root.resolve().relative_to(base).as_posix()}"
    except (ValueError, OSError):
        return str(skills_root)


# --------------------------------------------------------------------------
# Local state
# --------------------------------------------------------------------------


def state_path(skills_root: Path) -> Path:
    return skills_root / STATE_FILENAME


def read_state(skills_root: Path) -> dict[str, object]:
    """Read the release marker, tolerating absence and corruption."""
    path = state_path(skills_root)
    try:
        with open(long_path(path), encoding="utf-8") as handle:
            payload = json.loads(handle.read())
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeError, json.JSONDecodeError):
        # A damaged marker must never block an update; treat it as unknown.
        return {}
    return payload if isinstance(payload, dict) else {}


def installed_releases(skills_root: Path) -> dict[str, str]:
    """The release each installed skill was taken from, per the marker."""
    skills = read_state(skills_root).get("skills")
    if not isinstance(skills, dict):
        return {}
    return {
        name: tag
        for name, tag in skills.items()
        if isinstance(name, str)
        and isinstance(tag, str)
        and SKILL_NAME_PATTERN.fullmatch(name)
    }


def write_state(skills_root: Path, repository: str, tag: str, skills: dict[str, str]) -> None:
    """Record which release each installed AMRIT skill came from.

    Releases are versioned as a whole, so this stores the release tag per
    installed skill rather than inventing a separate per-skill version.
    """
    payload = {
        "repository": repository,
        "release": tag,
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "skills": dict(sorted(skills.items())),
    }
    path = state_path(skills_root)
    temporary = path.with_name(f"{STATE_FILENAME}.tmp")
    try:
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8"
        )
        os.replace(temporary, path)
    except OSError as error:
        raise UpdateError(f"Could not record the installed release in {path}: {error}")
    finally:
        if os.path.exists(long_path(temporary)):
            os.remove(long_path(temporary))


def installed_skill_names(skills_root: Path) -> list[str]:
    """AMRIT skills currently present on disk in this target."""
    if not os.path.isdir(long_path(skills_root)):
        return []
    try:
        entries = sorted(
            entry.name
            for entry in os.scandir(long_path(skills_root))
            if entry.is_dir()
        )
    except OSError as error:
        raise UpdateError(f"Could not read {skills_root}: {error}")
    return [name for name in entries if SKILL_NAME_PATTERN.fullmatch(name)]


# --------------------------------------------------------------------------
# Archive validation
# --------------------------------------------------------------------------


def is_symlink_entry(info: ZipInfo) -> bool:
    return stat.S_ISLNK(info.external_attr >> 16)


def validate_archive_member(name: str, skill_name: str) -> None:
    """Reject anything that could escape the destination directory."""
    if not name:
        raise UpdateError("the archive contains an entry with an empty name")
    if "\\" in name:
        raise UpdateError(f"the archive entry {name!r} contains a backslash")
    if name.startswith("/") or (len(name) > 1 and name[1] == ":"):
        raise UpdateError(f"the archive entry {name!r} is an absolute path")

    parts = PurePosixPath(name).parts
    if any(part == ".." for part in parts):
        raise UpdateError(f"the archive entry {name!r} escapes the skill directory")
    if not parts or parts[0] != skill_name:
        raise UpdateError(
            f"the archive entry {name!r} is outside the expected "
            f"'{skill_name}/' root directory"
        )


def validate_archive(package: Path, skill_name: str) -> None:
    """Confirm a downloaded package is exactly the skill it claims to be.

    Checked before anything on disk is touched.
    """
    try:
        with ZipFile(package) as archive:
            infos = archive.infolist()
    except (OSError, BadZipFile) as error:
        raise UpdateError(f"{skill_name}: the downloaded package is not a valid ZIP: {error}")

    if not infos:
        raise UpdateError(f"{skill_name}: the downloaded package is empty")

    for info in infos:
        if is_symlink_entry(info):
            raise UpdateError(
                f"{skill_name}: the archive entry {info.filename!r} is a symbolic link"
            )
        try:
            validate_archive_member(info.filename, skill_name)
        except UpdateError as error:
            raise UpdateError(f"{skill_name}: {error}") from None

    manifest = f"{skill_name}/{MANIFEST_KEY}"
    if manifest not in {info.filename for info in infos}:
        raise UpdateError(f"{skill_name}: the archive is missing {manifest}")


def long_path(path: Path) -> str:
    """A filesystem path safe to open even when it is long.

    Windows rejects paths over 260 characters unless they use the
    extended-length '\\\\?\\' form. Everywhere else the path is returned
    unchanged.
    """
    if os.name != "nt":
        return str(path)
    text = os.path.abspath(str(path))
    if text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def member_relative_path(name: str, skill_name: str) -> PurePosixPath | None:
    """An archive member's path relative to the skill root, or None for the root."""
    relative = PurePosixPath(name).relative_to(skill_name)
    return relative if relative.parts else None


def extract_archive(package: Path, skill_name: str, destination: Path) -> None:
    """Extract a validated package so that destination becomes the skill root.

    The archive's own '<skill>/' root component is stripped rather than
    reproduced inside a nested staging directory. That keeps the extracted
    paths as short as possible, which matters on Windows.
    """
    validate_archive(package, skill_name)
    remove_tree(destination)
    try:
        os.makedirs(long_path(destination), exist_ok=True)
        with ZipFile(package) as archive:
            for info in archive.infolist():
                relative = member_relative_path(info.filename, skill_name)
                if relative is None:
                    continue
                target = destination / relative
                if not is_inside(target, destination):
                    raise UpdateError(
                        f"{skill_name}: the archive entry {info.filename!r} "
                        "resolves outside the extraction directory"
                    )
                if info.is_dir():
                    os.makedirs(long_path(target), exist_ok=True)
                    continue
                os.makedirs(long_path(target.parent), exist_ok=True)
                with archive.open(info) as source:
                    with open(long_path(target), "wb") as sink:
                        shutil.copyfileobj(source, sink)
    except (OSError, ValueError, BadZipFile) as error:
        remove_tree(destination)
        raise UpdateError(f"{skill_name}: could not extract the package: {error}")
    except UpdateError:
        remove_tree(destination)
        raise

    if not os.path.isfile(long_path(destination / MANIFEST_KEY)):
        remove_tree(destination)
        raise UpdateError(f"{skill_name}: the extracted package has no {MANIFEST_KEY}")


def remove_tree(path: Path) -> None:
    """Delete a directory tree if it exists, ignoring a missing path."""
    target = long_path(path)
    if not os.path.exists(target):
        return
    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
    except OSError as error:
        raise UpdateError(f"Could not remove {path}: {error}")


# --------------------------------------------------------------------------
# Safe installation
# --------------------------------------------------------------------------


def install_skill(package: Path, skill_name: str, skills_root: Path) -> None:
    """Replace one skill directory, or leave the existing one exactly as it was.

    The package is validated, then extracted beside its destination inside the
    same skills root, so the final move is a same-filesystem rename. An existing
    installation is moved aside first and restored if the swap fails, so a
    failure never leaves a half-installed skill behind.
    """
    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        raise UpdateError(f"Refusing to install unexpected directory {skill_name!r}")

    try:
        os.makedirs(long_path(skills_root), exist_ok=True)
    except OSError as error:
        raise UpdateError(f"Could not create {skills_root}: {error}")

    destination = skills_root / skill_name
    # Short, fixed-length staging names. Embedding the skill name here would
    # add up to 40 characters to every extracted path, which pushes deep
    # installation targets past the Windows path limit.
    incoming = skills_root / f".amrit-incoming-{os.getpid()}"
    backup = skills_root / f".amrit-backup-{os.getpid()}"

    remove_tree(incoming)
    remove_tree(backup)
    extract_archive(package, skill_name, incoming)

    had_previous = os.path.exists(long_path(destination))
    if had_previous:
        try:
            os.rename(long_path(destination), long_path(backup))
        except OSError as error:
            remove_tree(incoming)
            raise UpdateError(
                f"{skill_name}: could not move the installed skill aside: {error}"
            )
    try:
        os.rename(long_path(incoming), long_path(destination))
    except OSError as error:
        remove_tree(incoming)
        if had_previous:
            try:
                os.rename(long_path(backup), long_path(destination))
            except OSError as restore_error:
                raise UpdateError(
                    f"{skill_name}: installation failed ({error}) and the "
                    f"previous copy could not be restored from {backup}: "
                    f"{restore_error}"
                ) from error
        raise UpdateError(f"{skill_name}: could not install the package: {error}")

    remove_tree(backup)


def download_package(
    release: Release, skill_name: str, directory: Path, fetcher: Fetcher
) -> Path:
    """Download one skill package into a temporary directory."""
    url = release.asset_url(skill_name)
    payload = fetcher(url, "application/octet-stream")
    if len(payload) > MAXIMUM_PACKAGE_BYTES:
        raise UpdateError(
            f"{skill_name}: the package at {url} exceeds the "
            f"{MAXIMUM_PACKAGE_BYTES // (1024 * 1024)} MiB limit"
        )
    if not payload:
        raise UpdateError(f"{skill_name}: the package at {url} was empty")
    package = directory / f"{skill_name}{PACKAGE_SUFFIX}"
    try:
        package.write_bytes(payload)
    except OSError as error:
        raise UpdateError(f"{skill_name}: could not save the download: {error}")
    return package


def select_skills(release: Release, requested: Sequence[str]) -> list[str]:
    """The skills to act on: every published one, or exactly those requested."""
    if not requested:
        return release.skill_names()
    for name in requested:
        release.asset_url(name)
    return list(requested)


def update_target(
    release: Release,
    skills_root: Path,
    requested: Sequence[str],
    repository: str,
    fetcher: Fetcher = default_fetcher,
    dry_run: bool = False,
    force: bool = False,
) -> list[SkillResult]:
    """Update one installation target, one skill at a time."""
    selected = select_skills(release, requested)
    recorded = installed_releases(skills_root)
    present = set(installed_skill_names(skills_root))
    results: list[SkillResult] = []
    installed: dict[str, str] = dict(recorded)
    changed = False

    for skill_name in selected:
        up_to_date = (
            not force
            and skill_name in present
            and recorded.get(skill_name) == release.tag
        )
        if up_to_date:
            results.append(SkillResult(skill_name, STATUS_CURRENT))
            continue
        if dry_run:
            results.append(SkillResult(skill_name, STATUS_PLANNED))
            continue

        try:
            with tempfile.TemporaryDirectory(prefix="amrit-skill-download-") as scratch:
                package = download_package(release, skill_name, Path(scratch), fetcher)
                install_skill(package, skill_name, skills_root)
        except UpdateError as error:
            results.append(SkillResult.failure(skill_name, str(error)))
            continue

        installed[skill_name] = release.tag
        changed = True
        results.append(SkillResult(skill_name, STATUS_UPDATED))

    if changed:
        write_state(skills_root, repository, release.tag, installed)
    return results


def check_target(
    release: Release, skills_root: Path, requested: Sequence[str]
) -> list[SkillResult]:
    """Report what an update would change, without touching anything."""
    selected = select_skills(release, requested)
    recorded = installed_releases(skills_root)
    present = set(installed_skill_names(skills_root))
    results: list[SkillResult] = []
    for skill_name in selected:
        if skill_name not in present:
            results.append(SkillResult(skill_name, STATUS_MISSING))
        elif recorded.get(skill_name) != release.tag:
            detail = recorded.get(skill_name, "unknown release")
            results.append(SkillResult(skill_name, STATUS_BEHIND, detail))
        else:
            results.append(SkillResult(skill_name, STATUS_CURRENT))
    return results


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def count_statuses(results: Iterable[SkillResult]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return counts


def report_results(label: str, results: Sequence[SkillResult]) -> None:
    print(f"Target: {label}")
    if not results:
        print("  (no skills selected)")
        print("")
        return
    for result in results:
        marker = STATUS_MARKERS.get(result.status, result.status)
        # ASCII only: a Windows console using a legacy code page mangles
        # characters such as an em dash.
        suffix = f" - {result.detail}" if result.detail else ""
        print(f"  [{marker}] {result.name}{suffix}")
    print("")


def report_summary(results: Sequence[SkillResult], checking: bool) -> None:
    counts = count_statuses(results)
    updated = counts.get(STATUS_UPDATED, 0)
    current = counts.get(STATUS_CURRENT, 0)
    planned = counts.get(STATUS_PLANNED, 0)
    behind = counts.get(STATUS_BEHIND, 0) + counts.get(STATUS_MISSING, 0)
    failed = counts.get(STATUS_FAILED, 0)

    if checking:
        if behind:
            print(f"{behind} AMRIT skill(s) can be updated.")
        else:
            print("AMRIT skills are already up to date.")
        return

    if planned:
        print(f"{planned} AMRIT skill(s) would be updated. Nothing was written.")
        return
    if failed:
        print(f"Installed {updated} AMRIT skill(s); {failed} failed.")
        return
    if updated:
        print(f"Installed {updated} AMRIT skill(s) successfully.")
        return
    if current:
        print("AMRIT skills are already up to date.")
        return
    print("No AMRIT skills were selected.")


# --------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Update the locally installed AMRIT skills from the latest GitHub "
            "Release. This is an explicit command; nothing updates in the "
            "background."
        ),
        epilog=(
            "Examples:\n"
            "  update-skills.sh                        update every AMRIT skill for Claude\n"
            "  update-skills.sh amrit-create-brd       update one skill\n"
            "  update-skills.sh create-brd             the same skill, by shorthand\n"
            "  update-skills.sh --all                  update Claude and agent targets\n"
            "  update-skills.sh --check                report available updates only\n"
            "  update-skills.sh --target ./.claude/skills\n"
            "                                          install into another project\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "skills",
        nargs="*",
        metavar="SKILL",
        help=(
            "Skills to update, for example 'amrit-create-brd'. The 'amrit-' "
            "prefix may be omitted. Every skill in the release is updated when "
            "omitted."
        ),
    )
    parser.add_argument(
        "--claude",
        action="store_true",
        help=(
            "Update the user-level Claude skills directory "
            f"(~/{TARGET_ROOTS[TARGET_CLAUDE].as_posix()}/). This is the default."
        ),
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help=(
            "Update the user-level agent skills directory "
            f"(~/{TARGET_ROOTS[TARGET_AGENTS].as_posix()}/), used by Cursor and "
            "Antigravity"
        ),
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_targets",
        help="Update both the Claude and the agent targets",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=None,
        metavar="DIRECTORY",
        help=(
            "Install into an explicit skills directory instead of a user-level "
            "target, for example another project's .claude/skills/. Cannot be "
            "combined with --claude, --agents, or --all"
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Report whether the installed skills are behind the latest release "
            "and exit without modifying anything"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be installed without downloading or writing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reinstall even when the recorded release already matches",
    )
    parser.add_argument(
        "--release",
        default=None,
        metavar="TAG",
        help=(
            "Install a specific release tag such as 'v1.0.3' instead of the "
            "latest release"
        ),
    )
    parser.add_argument(
        "--repository",
        default=DEFAULT_REPOSITORY,
        metavar="OWNER/NAME",
        help=f"Source repository (default: {DEFAULT_REPOSITORY})",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_skills",
        help="List the skills published in the resolved release, then exit",
    )
    return parser


def selected_targets(arguments: argparse.Namespace) -> list[str]:
    """Which named targets to act on, defaulting to Claude."""
    if arguments.target is not None:
        if arguments.claude or arguments.agents or arguments.all_targets:
            raise UpdateError(
                "--target cannot be combined with --claude, --agents, or --all"
            )
        return []
    if arguments.all_targets:
        return [TARGET_CLAUDE, TARGET_AGENTS]
    targets = []
    if arguments.claude:
        targets.append(TARGET_CLAUDE)
    if arguments.agents:
        targets.append(TARGET_AGENTS)
    return targets or [TARGET_CLAUDE]


def run(
    arguments: argparse.Namespace,
    repo_root: Path,
    fetcher: Fetcher = default_fetcher,
    home: Path | None = None,
) -> int:
    if arguments.check and arguments.dry_run:
        raise UpdateError("--check and --dry-run cannot be combined")

    repository = validate_repository(arguments.repository)
    requested = normalize_skill_names(arguments.skills)
    targets = selected_targets(arguments)

    roots: list[tuple[str, Path]] = []
    if arguments.target is not None:
        root = resolve_skills_root(arguments.target, None, repo_root, home=home)
        roots.append((describe_target(root, home=home), root))
    else:
        for target in targets:
            root = resolve_skills_root(None, target, repo_root, home=home)
            roots.append((describe_target(root, home=home), root))

    release = get_release(repository, arguments.release, fetcher)
    print(f"Latest release: {release.tag}" if arguments.release is None
          else f"Release: {release.tag}")
    print("")

    if arguments.list_skills:
        print(f"{len(release.assets)} skill package(s) published in {release.tag}:")
        for name in release.skill_names():
            print(f"  {name}")
        return 0

    everything: list[SkillResult] = []
    for label, root in roots:
        if arguments.check:
            results = check_target(release, root, requested)
        else:
            results = update_target(
                release,
                root,
                requested,
                repository,
                fetcher=fetcher,
                dry_run=arguments.dry_run,
                force=arguments.force,
            )
        report_results(label, results)
        everything.extend(results)

    report_summary(everything, checking=arguments.check)
    failed = [result for result in everything if result.status == STATUS_FAILED]
    if failed:
        print("", file=sys.stderr)
        for result in failed:
            print(f"error: {result.name}: {result.detail}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        return run(arguments, get_repo_root())
    except UpdateError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("", file=sys.stderr)
        print("error: interrupted; no further changes were made", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
