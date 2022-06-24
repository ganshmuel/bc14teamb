#/bin/bash
ENV_TYPE=$1
#(--env-file f"/test-env/bc14teamb/${BRANCH_NAME}/.env.${ENV_TYPE}")
docker compose --env-file "/test-env/compose-config-files/.env.billing.$ENV_TYPE"  \
 -f "/test-env/bc14teamb/billing/docker-compose.yml" -p "billing${ENV_TYPE}" up -d --build

docker compose --env-file "/test-env/compose-config-files/.env.weight.$ENV_TYPE"  \
 -f "/test-env/bc14teamb/weight/docker-compose.yml" -p "weight${ENV_TYPE}" up -d --build

