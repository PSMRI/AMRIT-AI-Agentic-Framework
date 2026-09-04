#!/usr/bin/env bash
#
# Update the locally installed AMRIT skills from the latest GitHub Release.
#
# An explicit developer command. It never polls, schedules, or updates
# anything in the background.
#
# Only 'amrit-*' skill directories are ever written. Skills from other
# frameworks, and skills the developer wrote, are left untouched.
#
# Usage:
#   ./scripts/update-skills.sh
#   ./scripts/update-skills.sh amrit-create-brd
#   ./scripts/update-skills.sh create-brd amrit-answer-codebase-questions
#   ./scripts/update-skills.sh --all
#   ./scripts/update-skills.sh --check
#   ./scripts/update-skills.sh --help

set -euo pipefail

script_directory="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/amrit-python.sh
source "${script_directory}/amrit-python.sh"

script_directory="$(amrit_scripts_directory "${BASH_SOURCE[0]}")"
python_command="$(amrit_python)"

exec "${python_command}" "${script_directory}/update-skills.py" "$@"
