from __future__ import absolute_import
from collections import OrderedDict


TRANSACTION_DICT = OrderedDict()


TRANSACTION_DICT["Customer First Name"] = lambda collection: collection["first_name"]
TRANSACTION_DICT["Customer Last Name"] = lambda collection: collection["last_name"]
TRANSACTION_DICT["Email ID"] = lambda collection: collection["email_id"]
TRANSACTION_DICT["Phone Number"] = lambda collection: collection["phone_number"]
TRANSACTION_DICT["Transaction Date"] = lambda collection: collection["transaction_date"]
TRANSACTION_DICT["Products List"] = lambda collection: collection["products"]
TRANSACTION_DICT["Paid Amount"] = lambda collection: collection["paid_amount"]

