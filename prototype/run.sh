#!/usr/bin/env bash
# One-word launcher for mindful-gate prototype.
# Bypasses venv activation/PATH issues by calling the venv's python3 directly.
cd "$(dirname "$0")"
exec .venv/bin/python3 main.py "$@"
