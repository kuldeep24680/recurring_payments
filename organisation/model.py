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
    email_id = db.StringField(max_length=255, required=True)
    created_at = db.DateTimeField()
    is_head_merchant = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    

    @classmethod
    def create_user(cls, username, password, email_id, is_head_merchant=False,is_admin=False):
        now = datetime.datetime.utcnow()
        user = OracleOrgUser(username=username, email_id=email_id, created_at=now)
        user.set_password(password)
        user.is_head_merchant = is_head_merchant
        user.is_admin=is_admin
        return user


class OracleOrgAvailableOffer(db.EmbeddedDocument):
    is_offer_available = db.BooleanField(required=True)
    start_date = db.DateTimeField()
    end_date = db.DateTimeField()
    discount_percent = db.IntField(default=0)


class OracleOrgServices(OracleDocumentABC):
    service_name = db.StringField()
    service_cost_per_month = db.FloatField()
    
    discount_offers = db.EmbeddedDocumentField(OracleOrgAvailableOffer, default=OracleOrgAvailableOffer)

    
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
    created_at = db.DateTimeField()
    phone_number = db.StringField()
    subscription_type = db.StringField()
    start_date = db.StringField()
    due_date = db.DateTimeField()
    service = db.ReferenceField(OracleOrgServices)
    payment = db.EmbeddedDocumentField(OracleOrgPayment, default=OracleOrgPayment)
    subscription_id = db.StringField()
    was_subscribed = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    card_details = db.EmbeddedDocumentField(OracleOrgCreditCardDetails, default=OracleOrgCreditCardDetails)
