import requests
import json

def postman(dict_res):
    address = "https://fhir-server.../XXXXXXXXXX"
    proxies = {
        "http": "http://XXXXXXXXXX",
        "https": "http://XXXXXXXXXX"
    }
    headers = {'Accept': 'application/fhir+json','Authorization': 'XXXXXXXXXX','Content-Type': 'application/fhir+json'}
    r = requests.get(address,proxies=proxies,headers=headers)

    r = requests.post(address,proxies=proxies,headers=headers,data=json.dumps(dict_res))
    print(r.status_code)
    print(r.text)
