#!/bin/bash

BRANCH_NAME=$1

cd /test-env/
git clone git@github.com:ganshmuel/bc14teamb.git &&\
cd /test-env/bc14teamb

git checkout $BRANCH_NAME --
git pull origin main

docker compose --env-file "/test-env/compose-config-files/.env.billing.dev"  \
 -f "/test-env/bc14teamb/billing/docker-compose.yml" -p "billingdev" up -d --build
docker compose --env-file "/test-env/compose-config-files/.env.weight.dev"  \
 -f "/test-env/bc14teamb/weight/docker-compose.yml" -p "weightdev" up -d --build


