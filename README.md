# نظام إدارة المراسلات — السكك الحديدية المصرية

[![CI](https://github.com/aymank2020/Automation-Secretariat-Railways-System/actions/workflows/ci.yml/badge.svg)](https://github.com/aymank2020/Automation-Secretariat-Railways-System/actions/workflows/ci.yml)

نظام داخلي لإدارة المراسلات (الوارد والصادر) لمكتب وكيل أول الوزارة للأمانة الفنية بالهيئة القومية لسكك حديد مصر.

- **Backend:** FastAPI 0.115 + SQLAlchemy 2 + PostgreSQL 16 + Alembic + Argon2 password hashing.
- **Frontend:** Vue 3 + Vite + Pinia + Tailwind CSS (RTL).
- **Auth:** JWT (HS256), admin-gated user creation, no public self-registration.
- **Deployment:** Docker Compose, with a Cloudflare-Tunnel-based architecture (no public ports needed).

---

## Quick start (local development)

Requires Docker + Docker Compose plugin.

```bash
git clone https://github.com/aymank2020/Automation-Secretariat-Railways-System.git
cd Automation-Secretariat-Railways-System
./start.sh                         # auto-generates dev creds in backend/.env
# OR
docker compose up --build          # SQLite + Vite dev server
```

- Frontend: <http://localhost:5173>
- Backend API: <http://localhost:8000>
- API docs: <http://localhost:8000/docs>

The dev launcher (`start.sh`) generates a strong random `SECRET_KEY` and a strong random `INITIAL_ADMIN_PASSWORD` on first run and prints them to `backend/.env`. There are **no** built-in default credentials.

### Run tests

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
SECRET_KEY=$(openssl rand -hex 32) pytest -q
```

---

## Production deployment (Ubuntu 24.04 LTS + Cloudflare Tunnel)

The production stack is Postgres + the FastAPI backend + an internal nginx that serves the built SPA and proxies `/api/*` to the backend, fronted by `cloudflared` so traffic enters via a private (or public) Cloudflare hostname.

### Architecture

```
Browser (with WARP)                Internet
        |                              |
        +----------- Cloudflare ------+
                          |
                cloudflared (outbound only)
                          |
        +-----------------v-----------------+
        | Server                            |
        | +------------+   +------------+   |
        | | frontend   |-->| backend     |  |
        | | (nginx)    |   | (FastAPI)   |  |
        | +-----+------+   +-----+------+   |
        |       |                |          |
        |       +-----+----------+          |
        |             v                     |
        |       +-----+------+              |
        |       | postgres   |              |
        |       +------------+              |
        +-----------------------------------+
```

- The server only opens **port 22** (SSH) on the public internet. Everything else is reached via the outbound Cloudflare Tunnel.
- `cloudflared` runs as a sibling container inside the same Docker network and forwards traffic to `http://frontend:80` (Docker DNS). Port 8080 is also bound to `127.0.0.1` of the host purely for local debugging.

### One-time bootstrap (Ubuntu 24.04)

On a freshly installed Ubuntu 24.04 server, with sudo access:

```bash
# 1. Pull the bootstrap script
curl -fsSL https://raw.githubusercontent.com/aymank2020/Automation-Secretariat-Railways-System/main/deploy/scripts/bootstrap-and-deploy.sh -o /tmp/bootstrap.sh
chmod +x /tmp/bootstrap.sh

# 2. Run as root, passing in the Cloudflare Tunnel token
sudo CLOUDFLARE_TUNNEL_TOKEN='eyJhIjoi...your-token...' /tmp/bootstrap.sh
```

The script will:

1. Update apt and install Docker, ufw, fail2ban, unattended-upgrades.
2. Configure ufw (deny incoming except 22), enable fail2ban for sshd.
3. Create a system user `railways` and clone the repo to `/opt/railways-secretariat`.
4. Generate a fresh `.env` with strong random secrets (`SECRET_KEY`, `POSTGRES_PASSWORD`, `INITIAL_ADMIN_PASSWORD`).
5. Build images and start the stack via `docker compose -f docker-compose.prod.yml up -d`.
6. Print the initial admin password (also saved to `/opt/railways-secretariat/INITIAL_CREDENTIALS.txt`, mode 600).

### Cloudflare side

1. Cloudflare Zero Trust → **Networks → Tunnels** → create a `cloudflared` tunnel; copy the install token.
2. In the same tunnel, **Public Hostnames** (or **Hostname routes** if private), set the service to `HTTP` and the URL to `http://frontend:80` (Docker service name) — `cloudflared` runs in the same Compose network and resolves it directly.
3. For private/internal access only, add team members to **Settings → WARP Client → Device enrollment**.

### Updating to the latest `main`

```bash
sudo bash /opt/railways-secretariat/deploy/scripts/update.sh
```

### Backups

```bash
sudo bash /opt/railways-secretariat/deploy/scripts/backup.sh
# -> /opt/backups/db-YYYYMMDD-HHMMSS.sql.gz
# -> /opt/backups/uploads-YYYYMMDD-HHMMSS.tar.gz
```

Schedule it via cron:

```cron
0 2 * * *  bash /opt/railways-secretariat/deploy/scripts/backup.sh >> /var/log/railways-backup.log 2>&1
```

### Logs and troubleshooting

```bash
cd /opt/railways-secretariat
sudo -u railways docker compose -f docker-compose.prod.yml ps
sudo -u railways docker compose -f docker-compose.prod.yml logs -f
sudo -u railways docker compose -f docker-compose.prod.yml logs cloudflared
```

### Recovering / rotating secrets

To rotate `SECRET_KEY` or the initial admin password, edit `/opt/railways-secretariat/.env` and run:

```bash
cd /opt/railways-secretariat
sudo -u railways docker compose -f docker-compose.prod.yml up -d --force-recreate backend
```

Rotating `SECRET_KEY` invalidates all existing JWTs — users must log in again.

---

## Security model

- Passwords are hashed with **Argon2id** via `argon2-cffi`. Existing SHA-256 hashes from earlier versions are auto-upgraded on next successful login.
- JWT signing key is loaded from the `SECRET_KEY` env var; the app fails to start if it is unset or shorter than 32 characters.
- `POST /auth/register` requires an admin token. Public self-registration is intentionally disabled.
- `seclevel` on register/create is sanitised server-side to `{admin, user}` to prevent privilege escalation.
- The Postgres container has no public port — only the backend reaches it via the internal Docker network.
- The frontend container binds only to `127.0.0.1` on the host.
- `cloudflared` makes purely outbound connections — no public inbound port is required.

---

## Project structure

```
.
├── backend/                # FastAPI service
│   ├── alembic/            # DB migrations
│   ├── app/                # application code
│   ├── tests/              # pytest smoke tests
│   ├── Dockerfile          # production image (non-root, healthcheck)
│   └── requirements.txt
├── frontend/               # Vue 3 SPA
│   ├── src/
│   ├── nginx.conf          # serves built SPA + proxies /api → backend
│   └── Dockerfile          # multi-stage build
├── deploy/scripts/
│   ├── bootstrap-and-deploy.sh   # idempotent first-boot provisioning
│   ├── update.sh                 # pull + rebuild + restart
│   └── backup.sh                 # nightly DB + uploads dumps
├── docs/                   # Arabic project docs (legacy)
├── docker-compose.yml      # local dev stack
├── docker-compose.prod.yml # production stack with cloudflared
├── .env.example            # production env template
└── README.md
```

---

## Older documentation

Arabic-language project notes from earlier milestones live under [`docs/`](./docs/).
