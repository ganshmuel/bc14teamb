#!/bin/bash
# curl -H "Content-Type: application/json" -X POST -d '{"username":"mkyong","password":"abc"}' http://localhost:8080/api/login/

curl="curl -s -I "localhost:8081"/health | grep HTTP/ | awk {'print '}"
result="true"
declare -a routes=("health" "weight" "unknown/")  # an array of the working api's
echo '' >log-test.txt
for api in "${routes[@]}"
    do
    i=$(curl -s -I "$1"/"$api" | grep HTTP/ | awk {'print '})   # "$1" is for dev team tests!!!
    logs="${api} >>>>>>>>> ${i}"
    echo ${logs} >> log-test.txt
    if [[ $i != *"HTTP/1.0 200 OK"* ]]
            then
            result="false"
        fi
    done

echo -e "${result}$(cat log-test.txt)" > log-test.txt
