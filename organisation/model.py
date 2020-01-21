from mongoengine import (
    StringField,
    BooleanField,
    DateTimeField)

from organisation.base_model import OracleDocumentABC, BaseUser
from oracle import db
from oracle.utils import generate_bcrypt_hash
import datetime
import bcrypt
from flask_login import UserMixin


class OracleOrgUser(BaseUser):
    username = db.StringField(max_length=255)
    created_at = db.DateTimeField()
    is_head_merchant = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    

class OracleOrgServices(OracleDocumentABC):
    service_name = db.StringField()
    code = db.StringField()
    service_cost_per_month = db.FloatField()
    is_offer_available = db.StringField()
    discount_percent = db.IntField(default=0)


class OracleOrgPayment(db.EmbeddedDocument):
    payment_status = db.BooleanField(default=False)
    is_paying_today = db.BooleanField(default=False)
    payment_mode = db.StringField()
    due_payment = db.FloatField()
    payment_pending_days = db.IntField(default=0)
    is_defaulter = db.BooleanField(default=False)
    transaction_id = StringField()
    

class OracleOrgCreditCardDetails(db.EmbeddedDocument):
    card_number = db.StringField()
    expiration_date = db.StringField()
    
    
class OracleOrgCustomer(OracleDocumentABC):
    first_name = db.StringField()
    last_name = db.StringField()
    email_id = db.StringField(max_length=255, required=True,unique=True)
    phone_number = db.StringField()
    subscription_type = db.StringField()
    start_date = db.StringField()
    due_date = db.StringField()
    service = db.ReferenceField(OracleOrgServices)
    payment = db.EmbeddedDocumentField(OracleOrgPayment, default=OracleOrgPayment)
    subscription_id = db.StringField()
    was_subscribed = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    card_details = db.EmbeddedDocumentField(OracleOrgCreditCardDetails, default=OracleOrgCreditCardDetails)
