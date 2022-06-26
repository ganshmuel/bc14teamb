import sys
import requests
import json
import random, string
from datetime import datetime



def createExpectedResponse(id, name, t1, t2, truckcount, session_count, products, agorot):
    return {
        "id": f"{id}",
        "name": f"{name}",
        "from": f"{t1}",
        "to": f"{t2}",
        "truckCount": f"{truckcount}",
        "sessionCount": f"{session_count}",
        "products": products,
        "total": f"{agorot}"
    }
def createProduct(product, count, amount, rate, pay):
    return {
        "product": f"{product}",
        "count": f"{count}",
        "amount": f"{amount}",
        "rate": f"{rate}",
        "pay": f"{pay}"
    }

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def main():
    BILLINGBASEPATH = 'http://localhost:8080'
    WEIGHTGBASEPATH = 'http://localhost:8081'


    #creates provider
    provider_name = randomword(10)
    body = {
        "name": f"{provider_name}"
    }
    response = requests.post(BILLINGBASEPATH + '/provider', json=body)
    response_dict = json.loads(response.text)
    provider_id = response_dict['id']

    #creates two trucks for provider
    truck_license1 = randomword(8)
    body = {
                "id": f"{truck_license1}",
                "provider_id": f"{provider_id}"
    }

    requests.post(BILLINGBASEPATH + '/truck', json=body)

    truck_license2 = randomword(8)
    body = {
        "id": f"{truck_license2}",
        "provider_id": f"{provider_id}"
    }
    requests.post(BILLINGBASEPATH + '/truck', json=body)
    path_for_bill = BILLINGBASEPATH + '/bill/' + provider_id


    # Test for empty bill and empty times
    response = requests.get(path_for_bill, json=body)
    print(json.loads(response.text))

    # Build expected response
    startDate = datetime.strptime(
        datetime.today().replace(day=1, hour=0, minute=0, second=0).strftime('%Y%m%d%H%M%S'),
        '%Y%m%d%H%M%S')
    expected_result = createExpectedResponse(provider_id, provider_name, startDate, "", 2, 6,[], 0)
    print(expected_result)

    #Test for illegal time t1
    #response = requests.get(path_for_bill + '?from=2022021521', json=body)



if __name__ == "__main__":
    main()