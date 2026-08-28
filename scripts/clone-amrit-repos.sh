#!/usr/bin/env bash
#
# Clone the configured AMRIT application repositories into the local,
# Git-ignored repos/ workspace.
#
# Safe to run repeatedly. An existing repository is reported and left
# untouched: never re-cloned, reset, cleaned, checked out, or pulled.
#
# Usage:
#   ./scripts/clone-amrit-repos.sh
#   ./scripts/clone-amrit-repos.sh Common-API HWC-API HWC-UI
#   ./scripts/clone-amrit-repos.sh --list
#   ./scripts/clone-amrit-repos.sh --dry-run

set -euo pipefail

script_directory="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/amrit-python.sh
source "${script_directory}/amrit-python.sh"

script_directory="$(amrit_scripts_directory "${BASH_SOURCE[0]}")"
python_command="$(amrit_python)"

exec "${python_command}" "${script_directory}/clone-amrit-repos.py" "$@"
