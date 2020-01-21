import logging
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
from oracle.settings import AUTHORIZE_CREDENTIALS

logger = logging.getLogger(__name__)


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
        # if there are no past transactions, arbTransactions will not exist, error should be handled.
        try:
            for transaction in response.subscription.arbTransactions.arbTransaction:
                print("Transaction id: %d" % transaction.transId)
                transaction_id = transaction.transId
                status = True
        except Exception as err:
            logger.error(err)
            transaction_id = ''
    else:
        print("response code: %s" % response.messages.resultCode)
        transaction_id = ''
    
    return status, transaction_id



