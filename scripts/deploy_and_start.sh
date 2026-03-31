#!/usr/bin/env bash
# PTS backend: Python 3.11.x (project validated on 3.11.9). See repo README.md and .python-version.
set -euo pipefail

PROJECT_ROOT="${1:-.}"
PORT="${PORT:-8000}"
BACKEND_PATH="$PROJECT_ROOT/backend"

if [ ! -d "$BACKEND_PATH" ]; then
  echo "Backend folder not found at $BACKEND_PATH"
  exit 1
fi

cd "$BACKEND_PATH"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created backend/.env from .env.example. Update credentials before production use."
fi

nohup python -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT" > backend.log 2>&1 &
echo "Backend started on port $PORT"
echo "Health check: http://localhost:$PORT/health"
