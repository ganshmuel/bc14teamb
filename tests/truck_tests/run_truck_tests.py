import sys
import requests
#--------------------TEST FOR POST -----------------


def main():
    BASEPATH = 'http://localhost:8080'
    path = BASEPATH + '/truck'

    # add provider to db

    body = {
        "name": "Nikolai"
    }
    requests.post(BASEPATH + '/provider', json=body)


    body = {
                "id": "5000",
                "provider_  id": "10001"
            }
    print(f"Success - Post {body} to Trucks")
    print(requests.post(path, json = body).status_code)
    body = {
        "id": "5000",
        "provider_id": "10001"
    }
    print(f"Failure. Try post {body} second time to Trucks")
    print(requests.post(path, json=body).status_code)

    body = {
        "id": "5000",
        "provider_id": "10020"
    }
    print(f"Failure - Try add {body}  with provider which doesn't exist")
    print(requests.post(path, json=body).status_code)

    body = {
        "id": "45484884888885555",
        "provider_id": "10001"
    }
    print(f"Failure - Try add {body}  with truck_id that is too long")
    print(requests.post(path, json=body).status_code)

    body = {
        "id": "",
        "provider_id": "10001"
    }

    print(f"Failure - Try add {body}  with provider which doesn't exist")
    print(requests.post(path, json=body).status_code)



if __name__ == "__main__":
    main()