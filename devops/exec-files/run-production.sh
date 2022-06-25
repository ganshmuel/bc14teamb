#!/bin/bash
BRANCH_NAME=$1

cd /test-env/
git clone git@github.com:ganshmuel/bc14teamb.git &&\
git config --global user.email "citestserer@devops.com"
git config --global user.name "citestserer"
git config --global init.defaultBranch main 
git config --global pull.rebase false
cd /test-env/bc14teamb
git checkout $BRANCH_NAME --
git pull origin main
git push origin main
git checkout main
docker compose --env-file "/test-env/compose-config-files/.env.${BRANCH_NAME}.prod"  \
-f "/test-env/bc14teamb/${BRANCH_NAME}/docker-compose.yml" -p "${BRANCH_NAME}prod" up -d --build
cd /test-env
rm -rf /test-env/bc14teamb