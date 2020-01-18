from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
from oracle.local_config import AUTHORIZE_CREDENTIALS


def get_recurring_payment_transaction_id(subscription_id):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = AUTHORIZE_CREDENTIALS["api_login_name"]
    merchantAuth.transactionKey = AUTHORIZE_CREDENTIALS["transaction_key"]
    getSubscription = apicontractsv1.ARBGetSubscriptionRequest()
    getSubscription.merchantAuthentication = merchantAuth
    getSubscription.subscriptionId = subscription_id
    getSubscription.includeTransactions = True
    getSubscriptionController = ARBGetSubscriptionController(getSubscription)
    getSubscriptionController.execute()
    status = False

    response = getSubscriptionController.getresponse()

    if response.messages.resultCode== "Ok":
        for transaction in response.subscription.arbTransactions.arbTransaction:
            print("Transaction id: %d" % transaction.transId)
            transaction_id = transaction.transId
            status = True
            
    else:
        print("response code: %s" % response.messages.resultCode)
        transaction_id = ''
    
    return status, transaction_id



