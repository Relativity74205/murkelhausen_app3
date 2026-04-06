#!/usr/bin/env bash
set -e

uv run python manage.py db_worker --no-reload --no-startup-delay
