#/bin/bash
ENV_TYPE=$1
BRANCH_NAME=$2

    cd /test-env/
    git clone git@github.com:ganshmuel/bc14teamb.git &&\
    cd /test-env/bc14teamb
    git checkout $BRANCH_NAME --
if [[ $ENV_TYPE == "prod" ]];then
    git pull origin main
    git push origin main
    git checkout main
    docker compose --env-file "/test-env/compose-config-files/.env.${BRANCH_NAME}.$ENV_TYPE"  \
    -f "/test-env/bc14teamb/billing/docker-compose.yml" -p "billing${ENV_TYPE}" up -d --build
else
    git checkout billing --
    docker compose --env-file "/test-env/compose-config-files/.env.billing.$ENV_TYPE"  \
     -f "/test-env/bc14teamb/billing/docker-compose.yml" -p "billing${ENV_TYPE}" up -d --build
    git checkout weight --
    docker compose --env-file "/test-env/compose-config-files/.env.weight.$ENV_TYPE"  \
     -f "/test-env/bc14teamb/weight/docker-compose.yml" -p "weight${ENV_TYPE}" up -d --build
    git checkout $BRANCH_NAME

fi