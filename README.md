# FLASK
Design a API for Credit card acceptance and validation

### Before running please install all required packages from requirement.txt file. File is available inside CreditCardAPI dir
> cd CreditCardAPI <br>
> pip install -r requirements.txt

### URL
> http://127.0.0.1:5000/v1/payment/

### Service accept only post method with below json body
```
    {
        'CreditCardNumber': card_no,
        'CardHolder': card_holder_name,
        'ExpirationDate': expiry_date,
        'SecurityCode': security_code,
        'Amount': amount
    }
```

#### Date format should be YYYY-MM-DD. 
##### Request will look like:

```
    {
        'CreditCardNumber': '1234432134560987',
        'CardHolder':'Shubham Shingare',
        'ExpirationDate': '2021-09-08',
        'SecurityCode': '123',
        'Amount': 5000
    }
```

# API Overview:
```
    1. ProcessPayment: main class where our API logic is written.


    2. Creted CustomerCardValidations class to validate all credit card details.
        a. credit_card: Validate credit card number
        b. exp_date: Validate date, Date should not less than current date
        c. security_code: Length of security code should be 3"""
        d. amount: Amount should not not negative


    3. Created dummy ServiceProvider class. It having three method.
        a. premium_payment_gateway: If the amount is > £500, try only 
                PremiumPaymentGateway and retry up to 3 times in case 
                payment does not get processed.
        
        b. expensive_payment_gateway: If the amount to be paid is £21-500,
                use ExpensivePaymentGateway if available. Otherwise, retry 
                only once with CheapPaymentGateway

        c. cheap_payment_gateway: If the amount to be paid is less than £20,
                use CheapPaymentGateway.
```