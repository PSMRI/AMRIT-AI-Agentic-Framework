#!/usr/bin/env bash
#
# Verify the local prerequisites for the AMRIT AI Agentic Framework.
#
# Framework setup only. Application repositories are cloned by
# scripts/clone-amrit-repos.sh, which this script can delegate to with
# --clone-repos. It never implements cloning itself.
#
# Usage:
#   ./scripts/install.sh
#   ./scripts/install.sh --validate
#   ./scripts/install.sh --clone-repos

set -euo pipefail

script_directory="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/amrit-python.sh
source "${script_directory}/amrit-python.sh"

script_directory="$(amrit_scripts_directory "${BASH_SOURCE[0]}")"
python_command="$(amrit_python)"

exec "${python_command}" "${script_directory}/install.py" "$@"
