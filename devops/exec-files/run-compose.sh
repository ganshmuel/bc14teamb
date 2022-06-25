#!/bin/bash

BRANCH_NAME=$1

    cd /test-env/
    git clone git@github.com:ganshmuel/bc14teamb.git &&\
#    git config --global user.email "citestserer@devops.com"
#    git config --global user.name "citestserer"
#    git config --global init.defaultBranch main 
#    git config --global pull.rebase false
    cd /test-env/bc14teamb
#    git checkout $BRANCH_NAME --
#if [[ $ENV_TYPE == *"prod"* ]];then
#    git pull origin main
#    git push origin main
#    git checkout main
#    docker compose --env-file "/test-env/compose-config-files/.env.${BRANCH_NAME}.$ENV_TYPE"  \
#    -f "/test-env/bc14teamb/${BRANCH_NAME}/docker-compose.yml" -p "${BRANCH_NAME}${ENV_TYPE}" up -d --build

git checkout billing --
docker compose --env-file "/test-env/compose-config-files/.env.billing.dev"  \
 -f "/test-env/bc14teamb/billing/docker-compose.yml" -p "billingdev" up -d --build
git checkout weight --
docker compose --env-file "/test-env/compose-config-files/.env.weight.dev"  \
 -f "/test-env/bc14teamb/weight/docker-compose.yml" -p "weightdev" up -d --build
git checkout $BRANCH_NAME

