#!/bin/bash
# ==============================================================================
# Oracle Cloud Always Free Deployment Script for Akshaya Embroidery AI
# ==============================================================================

set -e

echo "=========================================================="
echo "🚀 Starting Deployment on Oracle Cloud Always Free ARM VM"
echo "=========================================================="

# 1. Update system packages
echo "[1/5] Updating OS package lists..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Docker & Docker Compose if not installed
if ! command -v docker &> /dev/null; then
    echo "[2/5] Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo apt-get install -y docker-compose-plugin docker-compose
fi

# 3. Configure Oracle Linux / Ubuntu Firewall to open ports 80 & 443
echo "[3/5] Opening Ports 80 and 443 in iptables / ufw..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw reload || true
fi

# Oracle Ubuntu iptables rule fix
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT || true
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT || true
sudo netfilter-persistent save || true

# 4. Build & Run Docker Containers
echo "[4/5] Building & Launching App Containers with Docker Compose..."
sudo docker-compose up --build -d

# 5. Check Health
echo "[5/5] Checking container status..."
sudo docker-compose ps

echo "=========================================================="
echo "✅ Deployment Complete!"
echo "Your app is live at http://$(curl -s ifconfig.me)"
echo "=========================================================="
