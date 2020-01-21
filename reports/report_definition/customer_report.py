from __future__ import absolute_import
from collections import OrderedDict


PAYMENT_DICT = OrderedDict()


PAYMENT_DICT["Customer First Name"] = lambda collection: collection["first_name"]
PAYMENT_DICT["Customer Last Name"] = lambda collection: collection["last_name"]
PAYMENT_DICT["Subscription Type (in months)"] = lambda collection: collection[
    "subscription_type"
]
PAYMENT_DICT["Email ID"] = lambda collection: collection["email_id"]
PAYMENT_DICT["Service Name"] = lambda collection: collection["service_name"]
PAYMENT_DICT["Service Code"] = lambda collection: collection["code"]
PAYMENT_DICT["Payment Status"] = lambda collection: collection["payment_status"]
PAYMENT_DICT["Payment Mode"] = lambda collection: collection["payment_mode"]
PAYMENT_DICT["Due Amount"] = lambda collection: collection["due_amount"]
PAYMENT_DICT["Payment Pending Days"] = lambda collection: collection["payment_pending_days"]
PAYMENT_DICT["Phone Number"] = lambda collection: collection["phone_number"]
PAYMENT_DICT["Is Customer a Defaulter"] = lambda collection: collection["defaulter"]

