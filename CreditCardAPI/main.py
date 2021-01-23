from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from marshmallow import Schema, fields
from datetime import date
import random
from logger_config import get_logger


LOGGER = get_logger()
APP = Flask(__name__)
API = Api(APP)


ARGS = reqparse.RequestParser()
ARGS.add_argument("CreditCardNumber", type=str, help="Credit card number required", required=True)
ARGS.add_argument("CardHolder", type=str, help="Card holder name required", required=True)
ARGS.add_argument("ExpirationDate", type=str, help="Card Expiry date required", required=True)
ARGS.add_argument("SecurityCode", type=str, help="Security code", required=False)
ARGS.add_argument("Amount", type=float, help="Amount is required in numbers", required=True)


class ServiceProvider:
    def __init__(self, data):
        self.CreditCardNumber = data['CreditCardNumber']
        self.CardHolder = data['CardHolder']
        self.ExpirationDate = data['ExpirationDate']
        self.SecurityCode = data['SecurityCode']
        self.Amount = data['Amount']

    def premium_payment_gateway(self):
        """
        If the amount is > £500, try only PremiumPaymentGateway and
        retry up to 3 times in case payment does not get processed.
        """
        retries = 3
        response_list = [(404, 'FAIL', self.CreditCardNumber, 'PremiumPaymentGateway'),
                         (200, 'OK', self.CreditCardNumber, 'PremiumPaymentGateway')]
        while retries > 0:
            retries -= 1
            data = random.choice(response_list)
            if data[0] == 200:
                return [data]
        return [(404, 'FAIL', 'PremiumPaymentGateway')]

    def expensive_payment_gateway(self):
        """
        If the amount to be paid is £21-500, use ExpensivePaymentGateway if available.
        Otherwise, retry only once with CheapPaymentGateway
        """
        retries = 3
        response_list = [(404, 'FAIL', self.CreditCardNumber, 'ExpensivePaymentGateway'),
                         (200, 'OK', self.CreditCardNumber, 'ExpensivePaymentGateway')]
        while retries > 0:
            retries -= 1
            data = random.choice(response_list)
            if data[0] == 200:
                return [data]
        return [(404, 'FAIL', 'ExpensivePaymentGateway')]

    def cheap_payment_gateway(self):
        """
        If the amount to be paid is less than £20, use CheapPaymentGateway.
        """
        retries = 3
        response_list = [(404, 'FAIL', self.CreditCardNumber, 'CheapPaymentGateway'),
                         (200, 'OK', self.CreditCardNumber, 'CheapPaymentGateway')]
        while retries > 0:
            retries -= 1
            data = random.choice(response_list)
            if data[0] == 200:
                return [data]
        return [(404, 'FAIL', 'CheapPaymentGateway')]


class CustomerCardValidations:
    """Add your all custom validation here"""

    def credit_card(value):
        """
        Validate credit card number
        """
        # Length of credit card num should be 16
        if len(value) != 16:
            return False

        # isdigit() check all are number only
        # this will solve special character issue also
        elif not value.isdigit():
            return False

        # Check if all 16 digit are same i.e. 4444 4444 4444 44444
        elif value.isdigit():
            sum_of_digit = sum([int(i) for i in list(value)])
            if sum_of_digit == int(value[0]) * 16:
                return False

    def card_holder_name(name):
        """Validate card holder name"""
        if len(name) < 1:
            return False
        else:
            return True

    def exp_date(dt):
        """ Date hould not less than current date """
        if dt < date.today():
            return False
        else:
            return True

    def security_code(val):
        """Length of security code should be 3"""
        if len(val) == 3 and val.isdigit():
            return True
        else:
            return False

    def amount(val):
        """Amount should not not negative"""
        if not str(val).replace('.', '', 1).isdigit():
            return False
        elif val < 0:
            return False
        else:
            return True


class ResourceField(Schema):
    CreditCardNumber = fields.String(required=True, validate=CustomerCardValidations.credit_card)
    CardHolder = fields.String(required=True, validate=CustomerCardValidations.card_holder_name)
    ExpirationDate = fields.Date('%Y-%m-%d', required=True, validate=CustomerCardValidations.exp_date)
    SecurityCode = fields.String(required=True, validate=CustomerCardValidations.security_code)
    Amount = fields.Float(required=True, validate=CustomerCardValidations.amount)


class ProcessPayment(Resource):
    resourceFieldSchema = ResourceField()

    def post(self):
        args = ARGS.parse_args()
        LOGGER.info("Processing %s Card", args['CreditCardNumber'])
        errors = self.resourceFieldSchema.validate(args)
        if errors:
            LOGGER.error("Validation failed for %s Card, Failed validation is : %s",
                         args['CreditCardNumber'], errors)

            return abort(400, message=errors)
        # print(args)
        LOGGER.info("All validation passed for %s Card", args['CreditCardNumber'])
        service_provider = ServiceProvider(args)
        if args['Amount'] <= 20:
            LOGGER.info("Amount is less that 20 hence processing with CheapPaymentGateway using %s",
                        args['CreditCardNumber'])
            result = service_provider.cheap_payment_gateway()
        elif 20 < args['Amount'] <= 500:
            LOGGER.info("Amount is greater that 20 and Less that 500 hence processing with ExpensivePaymentGateway using %s",
                        args['CreditCardNumber'])
            result = service_provider.expensive_payment_gateway()
        elif args['Amount'] > 500:
            LOGGER.info("Amount is greater than 500 hence processing with PremiumPaymentGateway using %s",
                        args['CreditCardNumber'])
            result = service_provider.premium_payment_gateway()
        # print(result)
        LOGGER.info("Card %s payment result : %s", args['CreditCardNumber'], result)
        return 'ok'


API.add_resource(ProcessPayment, "/v1/payment/")
if __name__ == "__main__":
    APP.run(debug=True)
