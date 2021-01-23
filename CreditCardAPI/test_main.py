from main import APP
import unittest
import json


class MainApiTest(unittest.TestCase):

    def rest_call(self, data):
        url = '/v1/payment/'
        case = APP.test_client(self)
        response = case.post(url, data=data)
        return response

    def test_200_response(self):
        data1 = {'CreditCardNumber': '1234098745676543', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-04', 'SecurityCode': '123', 'Amount': 124}
        response = self.rest_call(data1)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_security(self):
        data1 = {'CreditCardNumber': '1234098745676543', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-04', 'SecurityCode': '1233', 'Amount': 124}
        response = self.rest_call(data1)
        status_code = response.status_code
        security = json.loads(response.data)['message']
        self.assertEqual(status_code, 400)
        self.assertIn('SecurityCode', security)

    def test_wrong_date_format(self):
        data1 = {'CreditCardNumber': '1234098745676543', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-44', 'SecurityCode': '123', 'Amount': 124}
        response = self.rest_call(data1)
        status_code = response.status_code
        expiry = json.loads(response.data)['message']
        self.assertEqual(status_code, 400)
        self.assertIn('ExpirationDate', expiry)

    def test_amount(self):
        data1 = {'CreditCardNumber': '1234098745676543', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-02', 'SecurityCode': '123', 'Amount': -124}
        response = self.rest_call(data1)
        status_code = response.status_code
        amount = json.loads(response.data)['message']
        self.assertEqual(status_code, 400)
        self.assertIn('Amount', amount)

    def test_amount_in_char(self):
        data1 = {'CreditCardNumber': '1234098745676543', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-02', 'SecurityCode': '123', 'Amount': "1234ff"}
        response = self.rest_call(data1)
        status_code = response.status_code
        amount = json.loads(response.data)['message']
        self.assertEqual(status_code, 400)
        self.assertIn('Amount', amount)

    def test_credit_card(self):
        data1 = {'CreditCardNumber': '8888888888888888', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-02', 'SecurityCode': '123', 'Amount': 124}
        response = self.rest_call(data1)
        status_code = response.status_code
        credit = json.loads(response.data)['message']
        self.assertIn('CreditCardNumber', credit)

    def test_wrong_data_keys(self):
        data1 = {'CreditCardNumber': '8888823888882388', 'CardHolder': 'Shubham Shingare',
                 'ExpirationDate': '2021-05-02', 'secuty': '123', 'Amount': 124}
        response = self.rest_call(data1)
        status_code = response.status_code
        credit = json.loads(response.data)['message']
        status_code = response.status_code
        self.assertEqual(status_code, 400)
        self.assertIn('SecurityCode', credit)



if __name__ == "__main__":
    unittest.main()
