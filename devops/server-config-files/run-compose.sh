#/bin/bash
docker compose -f "/weight/docker-compose.yml" -p "weight" up -d --build
docker compose -f "/billing/docker-compose.yml" -p "billing" up -d

