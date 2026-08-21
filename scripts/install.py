"""Check that this machine can run the AMRIT AI Agentic Framework.

Framework setup only. This script never clones, updates, or modifies an
application repository; cloning is delegated to clone-amrit-repos.py.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


MINIMUM_PYTHON = (3, 9)
MCP_FILES = (
    Path(".mcp.json"),
    Path(".cursor") / "mcp.json",
    Path(".agents") / "mcp_config.json",
)
TOKEN_PLACEHOLDER = "<put your token here>"
CLONE_SCRIPT = "clone-amrit-repos.py"
MANIFEST = Path("config") / "amrit-repositories.txt"
REQUIRED_DIRECTORIES = (
    Path("skills"),
    Path(".claude") / "skills",
    Path(".agents") / "skills",
    Path("scripts"),
)


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def report(ok: bool, message: str) -> bool:
    print(f"  [{'OK  ' if ok else 'FAIL'}] {message}")
    return ok


def check_python() -> bool:
    version = sys.version_info
    actual = f"{version.major}.{version.minor}.{version.micro}"
    required = ".".join(str(part) for part in MINIMUM_PYTHON)
    if version >= MINIMUM_PYTHON:
        return report(True, f"Python {actual} (minimum {required})")
    return report(False, f"Python {actual} is older than the required {required}")


def check_git() -> bool:
    try:
        completed = subprocess.run(
            ["git", "--version"], check=False, text=True, capture_output=True
        )
    except (OSError, subprocess.SubprocessError):
        return report(False, "Git was not found on PATH; install Git and re-run")
    if completed.returncode != 0:
        return report(False, "Git is present but 'git --version' failed")
    return report(True, completed.stdout.strip() or "Git is available")


def check_layout(repo_root: Path) -> bool:
    ok = True
    for relative in REQUIRED_DIRECTORIES:
        present = (repo_root / relative).is_dir()
        ok = report(present, f"{relative.as_posix()}/ present") and ok
    return ok


def check_manifest(repo_root: Path) -> bool:
    manifest = repo_root / MANIFEST
    if not manifest.is_file():
        return report(False, f"{MANIFEST.as_posix()} is missing")

    clone_module = load_clone_module(repo_root)
    try:
        entries = clone_module.read_manifest(manifest)
    except clone_module.ManifestError as error:
        return report(False, f"{MANIFEST.as_posix()} is unusable: {error}")
    return report(
        True, f"{MANIFEST.as_posix()} lists {len(entries)} application repositories"
    )


def check_workspace_is_ignored(repo_root: Path) -> bool:
    """Confirm the outer repository ignores the workspace directory."""

    probe = "repos/.bootstrap-check"
    try:
        completed = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", probe],
            cwd=str(repo_root),
            check=False,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.SubprocessError):
        return report(False, "Could not run 'git check-ignore' to verify repos/")
    if completed.returncode == 0:
        return report(True, "repos/ is ignored by this repository")
    return report(
        False,
        "repos/ is NOT ignored by this repository; add '/repos/' to .gitignore",
    )


def check_mcp_configuration(repo_root: Path) -> None:
    """Report MCP configuration state without ever printing a token value."""

    for relative in MCP_FILES:
        path = repo_root / relative
        if not path.is_file():
            print(f"  [note] {relative.as_posix()} is absent")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            print(f"  [note] {relative.as_posix()} could not be read: {error}")
            continue
        remaining = text.count(TOKEN_PLACEHOLDER)
        if remaining:
            print(
                f"  [note] {relative.as_posix()} still has {remaining} token "
                "placeholder(s) to fill in locally"
            )
        else:
            print(f"  [note] {relative.as_posix()} has no remaining placeholders")


def load_clone_module(repo_root: Path):
    import importlib.util

    script_path = repo_root / "scripts" / CLONE_SCRIPT
    spec = importlib.util.spec_from_file_location(
        "amrit_clone_repos", script_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    # Register before execution so dataclasses can resolve the module.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_repository_script(repo_root: Path, script: str, arguments: list[str]) -> int:
    command = [sys.executable, str(repo_root / "scripts" / script), *arguments]
    try:
        return subprocess.run(command, cwd=str(repo_root), check=False).returncode
    except (OSError, subprocess.SubprocessError) as error:
        print(f"error: could not run {script}: {error}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the local prerequisites for the AMRIT AI Agentic Framework."
        )
    )
    parser.add_argument(
        "--clone-repos",
        action="store_true",
        help=(
            "After a successful check, delegate to scripts/clone-amrit-repos.py "
            "to clone the configured application repositories"
        ),
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Also run scripts/validate-skills.py",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    repo_root = get_repo_root()

    print(f"AMRIT AI Agentic Framework setup check ({repo_root})")
    print("")
    print("Prerequisites")
    ok = check_python()
    ok = check_git() and ok

    print("")
    print("Repository layout")
    ok = check_layout(repo_root) and ok
    ok = check_manifest(repo_root) and ok
    ok = check_workspace_is_ignored(repo_root) and ok

    print("")
    print("MCP configuration (values are never displayed)")
    check_mcp_configuration(repo_root)

    if not ok:
        print("")
        print("Setup check FAILED. Resolve the items above and re-run.")
        return 1

    print("")
    print("Setup check passed.")

    if arguments.validate:
        print("")
        print("Running scripts/validate-skills.py")
        if run_repository_script(repo_root, "validate-skills.py", []) != 0:
            return 1

    if arguments.clone_repos:
        print("")
        print(f"Delegating to scripts/{CLONE_SCRIPT}")
        return run_repository_script(repo_root, CLONE_SCRIPT, [])

    print("")
    print("Next step: clone the AMRIT application repositories into repos/")
    print("  ./scripts/clone-amrit-repos.sh")
    print(f"  python scripts/{CLONE_SCRIPT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
