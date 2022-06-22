import requests
import json


def Create_Invoice(number):
	url = "http://localhost:8000/api/Create_Invoice"

	payload = json.dumps({
	  "number": number,
	  "generated_date": "2021-06-17",
	  "client": "123546879",
	  "employee": "159753456",
	  "company": "900541566"
	})
	headers = {
	  'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	print(response.text)

for i in range(10):
	Create_Invoice(i)
