#!/usr/bin/env bash
#
# Usage: . ./run_application.sh
# -----------------------------------------------------------------------------

export AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=us-east-2

python3.6 main_handler.py
