#/bin/bash
BRANCH_NAME=$1
ENV_TYPE=$2
#(--env-file f"/test-env/bc14teamb/${BRANCH_NAME}/.env.${ENV_TYPE}")
docker compose -p ${BRANCH_NAME}${ENV_TYPE} --env-file "/test-env/compose-config-files/.billing.env.$ENV_TYPE"  \
 -f "/test-env/bc14teamb/$BRANCH_NAME/docker-compose.yml" up -d --build



