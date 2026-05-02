#!/usr/bin/env bash
# ============================================================================
# Idempotent bootstrap + deploy for Ubuntu 24.04 LTS.
#
# Run on a fresh server as a sudo-capable user:
#
#   curl -fsSL <RAW_URL_OF_THIS_SCRIPT> -o bootstrap.sh
#   chmod +x bootstrap.sh
#   sudo CLOUDFLARE_TUNNEL_TOKEN='<TOKEN>' ./bootstrap.sh
#
# It is safe to re-run: every step is idempotent.
# ============================================================================
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/aymank2020/Automation-Secretariat-Railways-System.git}"
APP_USER="${APP_USER:-railways}"
APP_DIR="${APP_DIR:-/opt/railways-secretariat}"
BRANCH="${BRANCH:-main}"
# CIDR(s) allowed to reach the app on port 80, comma-separated.
# Default covers RFC1918 private ranges so any LAN can reach it,
# while UFW still blocks the public internet.
LAN_CIDRS="${LAN_CIDRS:-10.0.0.0/8,172.16.0.0/12,192.168.0.0/16}"

if [[ $EUID -ne 0 ]]; then
    echo "[!] This script must be run as root (use sudo)." >&2
    exit 1
fi

if [[ -z "${CLOUDFLARE_TUNNEL_TOKEN:-}" ]]; then
    if [[ -f "$APP_DIR/.env" ]] && grep -q '^CLOUDFLARE_TUNNEL_TOKEN=' "$APP_DIR/.env"; then
        : # ok, will reuse from existing .env
    else
        echo "[!] CLOUDFLARE_TUNNEL_TOKEN env var is required on first run." >&2
        echo "    Re-run as: sudo CLOUDFLARE_TUNNEL_TOKEN='<token>' $0" >&2
        exit 1
    fi
fi

log() { printf '\n\033[1;36m==>\033[0m %s\n' "$*"; }

# ----------------------------------------------------------------------------
log "Updating apt cache and installing base packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y upgrade
apt-get -y install \
    ca-certificates curl gnupg lsb-release git \
    ufw fail2ban unattended-upgrades \
    python3 openssl

# ----------------------------------------------------------------------------
log "Enabling unattended security upgrades"
dpkg-reconfigure -f noninteractive unattended-upgrades || true

# ----------------------------------------------------------------------------
log "Installing Docker Engine + compose plugin"
if ! command -v docker >/dev/null 2>&1; then
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    cat >/etc/apt/sources.list.d/docker.list <<EOF
deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable
EOF
    apt-get update
    apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi
systemctl enable --now docker

# ----------------------------------------------------------------------------
log "Creating dedicated non-root user '$APP_USER'"
if ! id -u "$APP_USER" >/dev/null 2>&1; then
    useradd --system --create-home --shell /bin/bash "$APP_USER"
fi
usermod -aG docker "$APP_USER"

# ----------------------------------------------------------------------------
log "Configuring UFW firewall (SSH + LAN-only HTTP; Cloudflare Tunnel is outbound)"
if ! ufw status | grep -q "Status: active"; then
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp comment "ssh"
    ufw --force enable
fi

# Make sure the LAN ranges have access to port 80 (idempotent).
IFS=',' read -ra _CIDRS <<<"$LAN_CIDRS"
for cidr in "${_CIDRS[@]}"; do
    cidr="$(echo "$cidr" | tr -d ' ')"
    [[ -z "$cidr" ]] && continue
    if ! ufw status | grep -q "80/tcp.*$cidr"; then
        ufw allow from "$cidr" to any port 80 proto tcp comment "lan-http"
    fi
done

# ----------------------------------------------------------------------------
log "Enabling fail2ban for sshd"
systemctl enable --now fail2ban

# ----------------------------------------------------------------------------
log "Cloning / updating repo into $APP_DIR"
mkdir -p "$APP_DIR"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

if [[ -d "$APP_DIR/.git" ]]; then
    sudo -u "$APP_USER" git -C "$APP_DIR" fetch --all --prune
    sudo -u "$APP_USER" git -C "$APP_DIR" checkout "$BRANCH"
    sudo -u "$APP_USER" git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
else
    sudo -u "$APP_USER" git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

# ----------------------------------------------------------------------------
log "Generating .env with strong random secrets (only on first run)"
ENV_FILE="$APP_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
    SECRET_KEY=$(openssl rand -hex 64)
    POSTGRES_PASSWORD=$(openssl rand -hex 32)
    INITIAL_ADMIN_PASSWORD=$(openssl rand -base64 18 | tr -d '/+=' | cut -c1-22)

    cat >"$ENV_FILE" <<EOF
POSTGRES_USER=railways_user
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=railways_hr

SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

ALLOW_ORIGINS=http://railways-secretariat,http://localhost:8080

INITIAL_ADMIN_USERNAME=admin
INITIAL_ADMIN_PASSWORD=$INITIAL_ADMIN_PASSWORD

CLOUDFLARE_TUNNEL_TOKEN=$CLOUDFLARE_TUNNEL_TOKEN

LOG_LEVEL=INFO
EOF
    chmod 600 "$ENV_FILE"
    chown "$APP_USER:$APP_USER" "$ENV_FILE"

    cat >"$APP_DIR/INITIAL_CREDENTIALS.txt" <<EOF
The initial admin user was created on first deploy.

  Username: admin
  Password: $INITIAL_ADMIN_PASSWORD

Please log in immediately and change this password from the user
settings page. After verifying, you can shred this file:

  shred -u INITIAL_CREDENTIALS.txt
EOF
    chmod 600 "$APP_DIR/INITIAL_CREDENTIALS.txt"
    chown "$APP_USER:$APP_USER" "$APP_DIR/INITIAL_CREDENTIALS.txt"
    echo "[+] First-run secrets written to $APP_DIR/.env (mode 600)."
    echo "[+] Initial admin password saved to $APP_DIR/INITIAL_CREDENTIALS.txt"
else
    echo "[i] $ENV_FILE already exists; leaving secrets as-is."
    if [[ -n "${CLOUDFLARE_TUNNEL_TOKEN:-}" ]]; then
        if grep -q '^CLOUDFLARE_TUNNEL_TOKEN=' "$ENV_FILE"; then
            sed -i "s|^CLOUDFLARE_TUNNEL_TOKEN=.*$|CLOUDFLARE_TUNNEL_TOKEN=$CLOUDFLARE_TUNNEL_TOKEN|" "$ENV_FILE"
        else
            echo "CLOUDFLARE_TUNNEL_TOKEN=$CLOUDFLARE_TUNNEL_TOKEN" >>"$ENV_FILE"
        fi
    fi
fi

# ----------------------------------------------------------------------------
log "Building images and starting the stack"
sudo -u "$APP_USER" -- bash -c "cd '$APP_DIR' && docker compose -f docker-compose.prod.yml pull cloudflared || true"
sudo -u "$APP_USER" -- bash -c "cd '$APP_DIR' && docker compose -f docker-compose.prod.yml up -d --build"

# ----------------------------------------------------------------------------
log "Waiting for stack health"
LAN_IP="$(ip -4 -o addr show scope global | awk '{print $4}' | cut -d/ -f1 | head -n1 || true)"
for _ in $(seq 1 30); do
    if curl --fail --silent --max-time 2 http://127.0.0.1/healthz >/dev/null; then
        echo "[+] Frontend nginx is healthy."
        break
    fi
    sleep 2
done

if curl --fail --silent --max-time 2 http://127.0.0.1/api/health >/dev/null; then
    echo "[+] Backend API reachable through frontend nginx."
else
    echo "[!] Backend not reachable yet via http://127.0.0.1/api/health"
    echo "    Run: sudo -u $APP_USER docker compose -f $APP_DIR/docker-compose.prod.yml logs backend"
fi

cat <<EOF

============================================================================
Deployment complete.

From the LAN (any device on the same network as this server):
  http://${LAN_IP:-<server-lan-ip>}

From outside the LAN (laptop on home Wi-Fi etc.):
  Install Cloudflare WARP, sign in to your Zero Trust team, then visit
  the same URL. WARP routes traffic through the secretariat tunnel.
  (Add a Private Network rule with CIDR ${LAN_IP:-<server-lan-ip>}/32 on
  the secretariat tunnel for this to work.)

Useful commands (run as the '$APP_USER' user or via sudo):
  cd $APP_DIR
  docker compose -f docker-compose.prod.yml ps
  docker compose -f docker-compose.prod.yml logs -f
  docker compose -f docker-compose.prod.yml logs cloudflared
  docker compose -f docker-compose.prod.yml restart

Update to latest main:
  sudo bash $APP_DIR/deploy/scripts/update.sh

Initial admin credentials (one-time):
  cat $APP_DIR/INITIAL_CREDENTIALS.txt
============================================================================
EOF
