'''
Paystack payment file
'''
import secrets
import requests
from procure.settings import PAYSTACK_TEST_KEY

HEADERS = {
    "Authorization": "Bearer "+ PAYSTACK_TEST_KEY,
}

def set_ref():
    '''
    Create reference code
    '''
    return secrets.token_urlsafe()


class Transaction:
    '''
    The Transactions API allows you create and manage payments on your integration
    '''
    def __init__(self, email, amount, currency="NGN"):
        self.reference = str(set_ref())
        self.amount = str(int(amount) * 100)
        self.currency = str(currency)
        self.email = str(email)
        self.body = {
            "email": email,
            "amount": self.amount,
            "reference": self.reference,
            "currency": self.currency,
            "channels": ["bank", "card", "ussd", "mobile_money", "bank_transfer", "qr"]
        }

    def initialize_transaction(self):
        '''
        Initialize a transaction from your backend
        '''
        url = "https://api.paystack.co/transaction/initialize"
        res = requests.post(url, headers=HEADERS, data=self.body)
        return res.json()


class Refund:
    '''
    Authorize refunds.
    '''
    def __init__(self, reference):
        self.body = {
            "transaction": reference
        }

    def create_refund(self):
        url = 'https://api.paystack.co/refund'
        res = requests.post(url, data=self.body, headers=HEADERS)
        return res.json()

def verify_payment(reference):
    '''
    Confirm the status of a transaction.
    '''
    url = "https://api.paystack.co/transaction/verify/"+ reference
    res = requests.get(url, headers=HEADERS)
    return res.json()

def get_transaction_detail(transaction_id):
    '''
    Get details of a transaction carried out on your integration.
    '''
    url = "https://api.paystack.co/transaction/" + transaction_id
    res = requests.get(url, headers=HEADERS)
    return res.json()

def get_transaction_timeline(transaction_id):
    '''
    View the timeline of a transaction
    '''
    url = "https://api.paystack.co/transaction/timeline/" + transaction_id
    res = requests.get(url, headers=HEADERS)
    return res.json()
