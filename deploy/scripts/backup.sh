#!/usr/bin/env bash
# Dump the Postgres DB and tar the uploads directory into /opt/backups.
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/railways-secretariat}"
BACKUP_DIR="${BACKUP_DIR:-/opt/backups}"
TS=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"

cd "$APP_DIR"

# DB dump
docker compose -f docker-compose.prod.yml exec -T postgres \
    pg_dump -U "$(grep ^POSTGRES_USER .env | cut -d= -f2)" \
            "$(grep ^POSTGRES_DB   .env | cut -d= -f2)" \
    | gzip > "$BACKUP_DIR/db-$TS.sql.gz"

# Uploads archive
docker run --rm \
    -v railways-secretariat_uploads_data:/source:ro \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf "/backup/uploads-$TS.tar.gz" -C /source .

echo "[+] Backups written to $BACKUP_DIR:"
ls -lh "$BACKUP_DIR" | tail -2
