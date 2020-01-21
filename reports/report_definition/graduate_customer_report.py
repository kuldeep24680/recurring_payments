from __future__ import absolute_import
from collections import OrderedDict


CUSTOMER_DICT = OrderedDict()


CUSTOMER_DICT["Customer First Name"] = lambda collection: collection["first_name"]
CUSTOMER_DICT["Customer Last Name"] = lambda collection: collection["last_name"]
CUSTOMER_DICT["Subscription Type (in months)"] = lambda collection: collection[
    "subscription_type"
]
CUSTOMER_DICT["Email ID"] = lambda collection: collection["email_id"]
CUSTOMER_DICT["Service Name"] = lambda collection: collection["service_name"]
CUSTOMER_DICT["Service Code"] = lambda collection: collection["service_code"]
CUSTOMER_DICT["Payment Status"] = lambda collection: collection["payment_status"]
CUSTOMER_DICT["Payment Mode"] = lambda collection: collection["payment_mode"]
CUSTOMER_DICT["Paid Amount"] = lambda collection: collection["paid_amount"]
CUSTOMER_DICT["Start Date"] = lambda collection: collection["start_date"]
CUSTOMER_DICT["Due Date"] = lambda collection: collection["due_date"]
CUSTOMER_DICT["Phone Number"] = lambda collection: collection["phone_number"]
