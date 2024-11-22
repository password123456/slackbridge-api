#!/bin/bash

PROG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VIRTUALENV_DIR="${PROG_DIR}/../venv"

source "${VIRTUALENV_DIR}/bin/activate"
python3 "${PROG_DIR}/collect_slackusers.py"
