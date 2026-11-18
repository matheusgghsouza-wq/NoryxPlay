#!/usr/bin/env bash
# Prepara uma VPS Ubuntu/Debian nova para rodar o NoryxPlay.
# Uso (como root, na VPS):  bash instalar-vps.sh https://github.com/SEU_USUARIO/SEU_REPO.git
set -euo pipefail
REPO="${1:?informe a URL do repositório}"

apt-get update -y
apt-get install -y python3 python3-venv git
id noryx >/dev/null 2>&1 || useradd --system --create-home --shell /usr/sbin/nologin noryx

if [ ! -d /opt/noryx ]; then
  git clone "$REPO" /opt/noryx
fi
cd /opt/noryx
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
[ -f config.yaml ] || cp config.example.yaml config.yaml
chown -R noryx:noryx /opt/noryx
cp deploy/noryx.service /etc/systemd/system/noryx.service
systemctl daemon-reload

echo
echo "Pronto. Agora:"
echo "  1) nano /opt/noryx/.env          (tokens)"
echo "  2) nano /opt/noryx/config.yaml   (contas, números, regras)"
echo "  3) cd /opt/noryx && sudo -u noryx .venv/bin/python main.py check"
echo "  4) systemctl enable --now noryx  (liga 24h)"
echo "  5) journalctl -u noryx -f        (acompanhar)"
