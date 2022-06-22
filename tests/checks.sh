#!/bin/bash

declare provider_name
declare response_code
declare host="ec2-3-88-220-120.compute-1.amazonaws.com"
declare port=8080

function check_response_code {
  if [ $1 -ne $2 ] ; then
	echo "RESULT: Test failed"
	echo "RESULT: Expected code $1, got code $2"
	exit 1
  else
	echo "RESULT: Pass"
	return 0
  fi
}

function generate_provider_name {
	provider_name="$(echo $RANDOM | md5sum | head -c 20)";
}

function generate_provider_name_int {
	provider_name="$RANDOM";
}

# Create a random provider and return its ID
function create_provider {
	generate_provider_name
	payload="$(jq --null-input --arg nm "$provider_name" '{"name": $nm}')"
	provider_id="$(curl -s -H 'Content-Type: application/json' --data "$payload" http://$host:$port/provider/ | jq -r .id)"
	echo $provider_id
}

# ----------- POST /Provider -----------

echo "TEST: POST /Provider, positive test"

# Generate a random provider name
generate_provider_name
# Preapre body
payload="$(jq --null-input --arg nm "$provider_name" '{"name": $nm}')"
# Prepare URL
url="http://$host:$port/provider/"
# Send request
response_code="$(curl -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data "$payload" $url)"
# Test response
check_response_code "200" "${response_code}"

echo "TEST: POST /Provider, negative test, provider name already exist"

# Send request
response_code="$(curl -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data "$payload" $url)"
# Test response
check_response_code "400" "${response_code}"

# ----------- PUT /Provider -----------

echo "TEST: PUT /Provider, positive test, change name to alphabetics"

# Create a random provider
provider_id=$(create_provider)
echo "LOG: Created new provider with ID $provider_id"
# Generate new name for existing provider
generate_provider_name
# Preapre body
payload="$(jq --null-input --arg nm "$provider_name" '{"name": $nm}')"
# Prepare URL
url="http://$host:$port/provider/$provider_id"
# Send request
response_code="$(curl -X PUT -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data "$payload" $url)"
echo "LOG: Changed provider ID $provider_id name to $provider_name"
# Test response
check_response_code "200" "${response_code}"

# ----------- POST /Rates -----------

filename="POST_rates_test"
url="http://$host:$port/rates"
payload="$(jq --null-input --arg nm "$filename" '{"file": $nm}')"
response_code="$(curl -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data "$payload" $url)"
check_response_code "200" "${response_code}"