import sys
import requests
import json
import random, string

#--------------------TEST FOR POST -----------------



def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def main():
    provider_name = randomword(10)
    truck_license = randomword(8)

    #-------- Send requests -------------
    BASEPATH = 'http://localhost:8080'
    path = BASEPATH + '/truck'

    # add provider to db

    body = {
        "name": f"{provider_name}"
    }

    response = requests.post(BASEPATH + '/provider', json=body)
    response_dict = json.loads(response.text)

    provider_id = response_dict['id']


    body = {
                "id": f"{truck_license}",
                "provider_id": f"{provider_id}"
            }
    print(f"Success - Post {body} to Trucks")
    print(requests.post(path, json = body).status_code)
    body = {
        "id": f"{truck_license}",
         "provider_id": f"{provider_id}"
    }
    print(f"Failure. Try post {body} second time to Trucks")
    print(requests.post(path, json=body).status_code)

    body = {
        "id": "5001",
        "provider_id": "100000"
    }
    print(f"Failure - Try add {body}  with provider which doesn't exist")
    print(requests.post(path, json=body).status_code)

    body = {
        "id": "45484884888885555",
        "provider_id": f"{provider_id}"
    }
    print(f"Failure - Try add {body}  with truck_id that is too long")
    print(requests.post(path, json=body).status_code)

    body = {
        "id": "",
        "provider_id": f"{provider_id}"
    }

    print(f"Failure - Try add {body}  with empty id")
    print(requests.post(path, json=body).status_code)


if __name__ == "__main__":
    main()