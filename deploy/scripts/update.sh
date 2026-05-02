#!/usr/bin/env bash
# Idempotent update: pulls main, rebuilds, restarts.
set -euo pipefail

APP_USER="${APP_USER:-railways}"
APP_DIR="${APP_DIR:-/opt/railways-secretariat}"
BRANCH="${BRANCH:-main}"

if [[ $EUID -ne 0 ]]; then
    echo "[!] Run as root (sudo)." >&2
    exit 1
fi

cd "$APP_DIR"
sudo -u "$APP_USER" git fetch --all --prune
sudo -u "$APP_USER" git checkout "$BRANCH"
sudo -u "$APP_USER" git pull --ff-only origin "$BRANCH"

sudo -u "$APP_USER" -- bash -c "cd '$APP_DIR' && docker compose -f docker-compose.prod.yml pull cloudflared || true"
sudo -u "$APP_USER" -- bash -c "cd '$APP_DIR' && docker compose -f docker-compose.prod.yml up -d --build"
sudo -u "$APP_USER" -- bash -c "cd '$APP_DIR' && docker image prune -f"

echo "[+] Update complete."
