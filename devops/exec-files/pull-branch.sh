#/bin/bash
 
cd /test-env/bc14teamb
echo log1 $@ >> logs.txt
git checkout devops
git pull origin $1

