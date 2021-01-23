import requests
from datetime import date

BSE = "http://127.0.0.1:5000/v1/payment/"

data = {"CreditCardNumber": "6666666664666464",
        "CardHolder": "Shubham Shingare",
        "ExpirationDate": "2021-05-04",
        "SecurityCode": "123",
        "Amount": 124}
# print(date.today())
res = requests.post(BSE, data=data)
print(res.json())