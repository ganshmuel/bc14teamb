#!/bin/bash

# curl -H "Content-Type: application/json" -X POST -d '{"username":"mkyong","password":"abc"}' http://localhost:8080/api/login/
result="true"
curl="curl -s -I localhost:8081/health | grep HTTP/ | awk {'print '}"
result="true"
declare -a routes=("health" "weight" "unknown/")

for api in "${routes[@]}"
    do
    i=$(curl -s -I localhost:8081/"$api" | grep HTTP/ | awk {'print '})
    if [[ $i != *"HTTP/1.0 200 OK"* ]]
            then
            result="false"
        fi
    done


echo $result > log-test.txt



# for api in ${routes}
#     do
#     $api $api
#     echo $result
#     done