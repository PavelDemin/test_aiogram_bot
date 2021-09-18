#!/usr/bin/env bash

set -e

PYTHON="python -O"

${PYTHON} -m app.utils.before_start
alembic upgrade head
${PYTHON} -m app