import os, sys
import imp

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from oracle.local_config import AUTHORIZE_CREDENTIALS


def cancel_subscription(subscriptionId):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = AUTHORIZE_CREDENTIALS["api_login_name"]
    merchantAuth.transactionKey = AUTHORIZE_CREDENTIALS["transaction_key"]

    request = apicontractsv1.ARBCancelSubscriptionRequest()
    request.merchantAuthentication = merchantAuth
    request.refId = "Sample"
    request.subscriptionId = subscriptionId

    controller = ARBCancelSubscriptionController(request)
    controller.execute()

    response = controller.getresponse()

    if response.messages.resultCode == "Ok":
        print("Message Code : %s" % response.messages.message[0]['code'].text)
        print("Message text : %s" % response.messages.message[0]['text'].text)
        return True
    else:
        print("Message Code : %s" % response.messages.message[0]['code'].text)
        print("Message text : %s" % response.messages.message[0]['text'].text)
        return False
