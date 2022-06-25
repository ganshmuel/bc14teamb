#/bin/bash
BRANCH_NAME=$1
cd /test-env/
git clone git@github.com:ganshmuel/bc14teamb.git &&\
cd /test-env/bc14teamb
git checkout $BRANCH_NAME --


