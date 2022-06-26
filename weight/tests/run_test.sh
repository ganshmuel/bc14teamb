#!/bin/bash

post_curl="curl -I -X POST "http://localhost:8081/batch-weight?file=containers1.csv" 2>&1 | grep -i http|tail -n1"
get_curl="curl -s -I "localhost:8081"/health | grep HTTP/ | awk {'print '}"
result="true"

declare -a get_routes=("health" "weight" "unknown/" "item/87/" "session/10001")  # an array of the working api's
declare -a post_routes=("batch-weight?file=containers1.csv")


echo '' >log-test.txt


##########----  get requests tests ----##########

for api in "${get_routes[@]}"
    do
    i=$(curl -s -I "$1"/"$api" | grep HTTP/ | awk {'print '})   # "$1" is for dev team tests!!!
    logs="${api} >>>>>>>>> ${i}"
    echo "${logs}" >> log-test.txt
    if [[ $i != *"HTTP/1.0 200 OK"* ]]
            then
            result="false"
        fi
    done
##########----  get requests tests ----##########


for api in "${post_routes[@]}"
    do
    y=$(curl -I -X POST "$1"/"$api" 2>&1 | grep -i http | tail -n1)  # "$1" is for dev team tests!!!
    logs="${api} >>>>>>>>> ${y}"
    echo "${logs}" >> log-test.txt
    if [[ $y != *"HTTP/1.0 200 OK"* ]]
            then
            result="false"
        fi
    done
echo -e "${result}$(cat log-test.txt)" > log-test.txt




# curl -I -X POST "http://localhost:8081/batch-weight?file=containers1.csv" 2>&1 | grep -i http|tail -n1


