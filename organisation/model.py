from mongoengine import (
    StringField,
    BooleanField)

from organisation.base_model import OracleDocumentABC
from oracle import db
from oracle.utils import generate_bcrypt_hash
import datetime
import bcrypt


class OracleOrgMerchant(OracleDocumentABC):
    name = db.StringField()
    username = db.StringField(max_length=255, required=True)
    email_id = db.StringField(max_length=255, required=True)
    password = StringField(max_length=128, required=True)
    is_head_merchant = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    
    meta = {"abstract": True}

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        self.password = generate_bcrypt_hash(raw_password)

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """

        return str(self.password).encode() == bcrypt.hashpw(
            str(raw_password).encode("utf-8"), str(self.password).encode("utf-8")
        )

    @classmethod
    def create_user(cls, username, password):
        now = datetime.datetime.utcnow()
        user = OracleOrgMerchant(username=username, created_at=now)
        user.set_password(password)
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
    email_id = db.StringField(max_length=255, required=True)
    phone_number = db.StringField()
    subscription_type = db.StringField()
    start_date = db.StringField()
    due_date = db.DateTimeField()
    service = db.ReferenceField(OracleOrgServices)
    payment = db.EmbeddedDocumentField(OracleOrgPayment, default=OracleOrgPayment)
    subscription_id = db.StringField()
    card_details = db.EmbeddedDocumentField(OracleOrgCreditCardDetails, default=OracleOrgCreditCardDetails)

