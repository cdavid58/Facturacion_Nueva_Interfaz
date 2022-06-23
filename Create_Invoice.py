import requests
import json

def Create(number):
  url = "http://localhost:8000/api/Create_Invoice"

  payload = json.dumps({
    "invoice": {
      "number": number,
      "generated_date": "2022-06-17",
      "client": "123546879",
      "employee": "159753456",
      "company": "900541566"
    },
    "details": [
      {
        "product": "All One Lenovo",
        "quanty": 5,
        "tax": 19,
        "cost": 0.94,
        "discount": 0,
        "ico": 0,
        "stronghold": 0,
        "payment_method": 10,
        "payment_due_date": "2022-06-17",
        "duration_measure": 0,
        "price":3800
      },
      {
        "product": "All One Lenovo",
        "quanty": 5,
        "tax": 19,
        "cost": 0.94,
        "discount": 0,
        "ico": 0,
        "stronghold": 0,
        "payment_method": 10,
        "payment_due_date": "2022-06-17",
        "duration_measure": 0,
        "price":3800
      }
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(number)
  print(response.text)




for i in range(1):
  Create(i)