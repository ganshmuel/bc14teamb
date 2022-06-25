#/bin/bash
cd /test-env
git clone git@github.com:ganshmuel/bc14teamb.git && \
cd bc14teamb
git config --global user.email "citestserer@devops.com"
git config --global user.name "citestserer"
git config --global init.defaultBranch main 
git config --global pull.rebase false



