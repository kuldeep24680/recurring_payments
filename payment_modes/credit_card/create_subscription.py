from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
from datetime import *
from oracle.local_config import AUTHORIZE_CREDENTIALS


def create_subscription(**kwargs):
    # Setting the merchant details
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = AUTHORIZE_CREDENTIALS["api_login_name"]
    merchantAuth.transactionKey = AUTHORIZE_CREDENTIALS["transaction_key"]
    # Setting payment schedule
    paymentschedule = apicontractsv1.paymentScheduleType()
    paymentschedule.interval = apicontractsv1.paymentScheduleTypeInterval()
    paymentschedule.interval.length = kwargs.get("number_days")
    paymentschedule.interval.unit = apicontractsv1.ARBSubscriptionUnitEnum.days
    paymentschedule.startDate = datetime.strptime(kwargs.get("start_date"), "%d/%m/%Y")  # datetime(2020, 8, 30)
    paymentschedule.totalOccurrences = 12
    paymentschedule.trialOccurrences = 1
    # Giving the credit card info
    creditcard = apicontractsv1.creditCardType()
    creditcard.cardNumber = kwargs.get("card_number")  # "4111111111111111"
    creditcard.expirationDate = kwargs.get("expiration_date")  # "2020-12"
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditcard
    # Setting billing information
    billto = apicontractsv1.nameAndAddressType()
    billto.firstName = kwargs.get("first_name")
    billto.lastName = kwargs.get("last_name")
    # Setting subscription details
    subscription = apicontractsv1.ARBSubscriptionType()
    subscription.name = "Sample Subscription"
    subscription.paymentSchedule = paymentschedule
    subscription.amount = kwargs.get("due_amount")
    subscription.trialAmount = Decimal('0.01')
    subscription.billTo = billto
    subscription.payment = payment
    # Creating the request
    request = apicontractsv1.ARBCreateSubscriptionRequest()
    request.merchantAuthentication = merchantAuth
    request.subscription = subscription
    # Creating and executing the controller
    controller = ARBCreateSubscriptionController(request)
    controller.execute()
    # Getting the response
    response = controller.getresponse()
    
    if response.messages.resultCode == "Ok":
        print("SUCCESS:")
        print("Message Code : %s" % response.messages.message[0]['code'].text)
        print("Message text : %s" % str(response.messages.message[0]['text'].text))
        print("Subscription ID : %s" % response.subscriptionId)
        return True, response.subscriptionId
    else:
        print("ERROR:")
        print("Message Code : %s" % response.messages.message[0]['code'].text)
        print("Message text : %s" % response.messages.message[0]['text'].text)
        return False, ''
