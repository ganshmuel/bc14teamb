#/bin/bash

docker compose -f "/tests/docker-compose.yml" up && echo "success"
