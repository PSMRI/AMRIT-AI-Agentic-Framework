#!/usr/bin/env bash
# Shared helpers for the framework's POSIX entry points.
#
# Sourced by install.sh and clone-amrit-repos.sh so neither duplicates
# repository-root discovery or Python interpreter selection.

set -euo pipefail

# Absolute path of the scripts/ directory containing the calling script.
amrit_scripts_directory() {
    local source_path="$1"
    while [ -L "$source_path" ]; do
        local link_target
        link_target="$(readlink "$source_path")"
        case "$link_target" in
            /*) source_path="$link_target" ;;
            *) source_path="$(cd -P "$(dirname "$source_path")" && pwd)/$link_target" ;;
        esac
    done
    cd -P "$(dirname "$source_path")" && pwd
}

# First usable Python 3 interpreter on this machine.
amrit_python() {
    local candidate
    for candidate in python3 python py; do
        if command -v "$candidate" >/dev/null 2>&1; then
            if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' \
                >/dev/null 2>&1; then
                printf '%s\n' "$candidate"
                return 0
            fi
        fi
    done
    printf 'error: Python 3.9 or newer is required but was not found on PATH.\n' >&2
    return 1
}
