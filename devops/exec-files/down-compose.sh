#/bin/bash
#(--env-file f"/test-env/bc14teamb/${BRANCH_NAME}/.env.${ENV_TYPE}")
docker compose -f "/test-env/bc14teamb/billing/docker-compose.yml" -p "billingdev" down 

docker compose -f "/test-env/bc14teamb/weight/docker-compose.yml" -p "weightdev"  down 

cd /test-env/bc14teamb/
rm -fr ./billing ./weight
docker system prune -f


