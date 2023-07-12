#!/bin/sh

set -e

poetry install
poetry run rq worker --url redis://redis:6379 --with-scheduler &
poetry run python workers/periodic_toot.py &
poetry run python workers/follow_back.py &
