#!/bin/bash

declare provider_name
declare response_code
#declare host="ec2-54-226-67-144.compute-1.amazonaws.com"
declare host="localhost"
declare port=8080
declare package_name=jq


# Returns true if Linux distro is Ubuntu
function os_is_ubuntu {
	if lsb_release -d | grep -q Ubuntu; then
		return 0;
	else
		return 1;
	fi
}

# Check if jq is installed, if not - install it
function install_jq {
	if os_is_ubuntu; then
		if ! dpkg -s $package_name &> /dev/null ;then
			echo "Package $package_name not found and is needed, will install it now"
			sudo apt-get -qq install $package_name
		fi
    fi
}

install_jq

function check_response_code {
  if [[ $1 -ne $2 ]] ; then
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


# Get random provider and truck by given truck license plate, return response status code
function create_truck {
    declare license_plate="$1"
	# Create a random provider
	provider_id=$(create_provider)
	# Prepare URL
	url=" http://$host:$port/truck/"
	# Preapre body
	payload="$(jq --null-input --arg pid "$provider_id" '{"provider_id": $pid, "id": "$license_plate"}')"
	# Send request
	response_code="$(curl -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data "$payload" $url)"
	echo $response_code
}


# ----------- POST /truck -----------

echo "TEST: POST /truck, positive test"
# Generate a random truck's license plate
#truck_id="$RANDOM"
# Create provider and truck
#response_code="$(create_truck $truck_id)"

#Run tests with for different input(see result in)
(python3 billing/tests/truck_tests/run_truck_tests.py) > billing/tests/truck_tests/tests_results.txt
#Compare results with expected values
(python3 billing/tests/truck_tests/check_truck_tests.py) > billing/tests/truck_tests/result.txt
response_code=`cat billing/tests/truck_tests/result.txt`
# Validate result
check_response_code "200" "${response_code}"



#-------------GET / BILL ---------------

echo "TEST: GET / BILL, positive test"


(python3 billing/tests/bill_tests/run_bill_tests.py) > billing/tests/bill_tests/bill_results.txt
#Compare results with expected values
(python3 billing/tests/bill_tests/check_bill_tests.py) > billing/tests/bill_tests/result.txt
response_code=`cat billing/tests/bill_tests/result.txt`
# Validate result
check_response_code "200" "${response_code}"



# ----------- POST /Provider -----------

echo "TEST: POST /Provider, positive test"

# Generate a random provider name
generate_provider_name
# Preapre body
payload="$(jq --null-input --arg nm "$provider_name" '{"name": $nm}')"
echo ${payload}
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



# ----------- PUT /trucks/<truck_id> -----------

#echo "TEST: PUT /trucks/<truck_id>, positive test"
#
## Create truck
#
## Generate a random truck's license plate
#truck_id="$RANDOM"
## Create provider and truck
## Create new provider
#provider_id=$(create_provider)
#response_code="$(create_truck $provider_id $truck_id)"
## Validate result
#check_response_code "200" "${response_code}"




# ----------- POST /rates -----------

#echo "TEST: POST /rates, positive test"
#
filename="POST_rates_test"
url="http://$host:$port/rates"
payload="$(jq --null-input --arg nm "$filename" '{"file": $nm}')"
response_code="$(curl -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data "$payload" $url)"
check_response_code "200" "${response_code}"

# ----------- GET /rates -----------

echo "TEST: GET /rates, positive test"

curl -s "http://$host:$port/rates" | jq -r .message | grep -q "was generated"


# Update truck
echo "TEST: PUT //trucks/<truck_id>, positive test"
# carate a random provider and truck id
provider_id=$(create_provider)
truck_id="$RANDOM"
payload="$(jq --null-input --arg nm "$truck_id" '{"id": $nm , "provider_id": '$provider_id'}')"
curl -s -H 'Content-Type: application/json' --data "$payload" http://$host:$port/truck/
# Prepare URL
url=" http://$host:$port/trucks/$truck_id"
# Send request
response_code="$(curl -X PUT -o /dev/null -s -w "%{http_code}\n" -H "Content-Type: application/json" --data {\"provider_id\":\"$provider_id\"} $url)"
# Test response
check_response_code "200" "${response_code}"


check_response_code 0 $?
