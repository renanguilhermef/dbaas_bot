#!/bin/bash
apt-get update
apt-get install -y docker.io docker-compose git
usermod -aG docker $USER
cd /home/${USER}
git clone https://github.com/YOUR_GITHUB_USER/YOUR_REPO.git dbaas_bot
cd dbaas_bot
docker compose up -d --build