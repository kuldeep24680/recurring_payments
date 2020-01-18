from datetime import datetime

from wtforms import (PasswordField,
    HiddenField,
    ValidationError,
    IntegerField,
    SelectField,
    BooleanField,
    StringField,
    FloatField,
    DateTimeField
)
from wtforms import SelectMultipleField, Form
from wtforms import validators as v

from organisation.model import OracleOrgCustomer, OracleOrgPayment, OracleOrgServices, OracleOrgAvailableOffer, \
    OracleOrgCreditCardDetails

subscription_type_dict = {
    "Monthly": 1,
    "Quarterly": 3,
    "Half Yearly": 6,
    "Yearly": 12,
}


class AddOrganisationCustomerForm(Form):
    first_name = StringField(validators=[v.Length(max=255)])
    last_name = StringField(validators=[v.Length(max=255)])
    email_id = StringField(validators=[v.email()])

    subscription_type_option = [
        (1, "Monthly"),
        (3, "Quarterly"),
        (6, "Half Yearly"),
        (12, "Yearly")
    ]
    subscription_type = SelectField(choices=subscription_type_option)
    phone_number = StringField(validators=[v.Length(max=15)])
    start_date = StringField()
    due_date = StringField()
    service_name = StringField()
    payment_mode = SelectField(
        choices=[("subscription", "Subscription Based"), ("cash", "Cash")]
    )
    card_nummber = StringField()
    expiration_date = StringField()

    def validate(self):
        email_id = self.email_id.data
        if OracleOrgCustomer.objects.filter(email_id=email_id):
            return False, u"Product with this name Already exists"

    def save(self, customer=None):
        if customer:
            cust = customer
        else:
            cust = OracleOrgCustomer(email_id=self.email_id.data)
        now = datetime.datetime.utcnow()
        service = OracleOrgServices.objects.get(id=self.service.data)
        cust.first_name = self.first_name.data
        cust.last_name = self.last_name.data
        cust.phone_number = self.phone_number.data
        cust.subscription_type = self.subscription_type.data
        cust.start_date = datetime.strptime(self.start_date.data, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%Y")
        cust.due_date = datetime.strptime(self.due_date.data, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%Y")
        cust.service = service
        cust.payment_mode = self.payment_mode.data
        cust.created_at = now
        cust.product = OracleOrgPayment(
            payment_status = False,
            is_paying_today = False,
            payment_mode = self.payment_mode.data,
            due_payment = float(service.service_cost_per_month*subscription_type_dict[self.subscription_type.data]),
            payment_pending_days = 0,
            is_defaulter = False,
            transaction_id = None
        )
        if self.payment_mode.data == "Subscription Based":
            cust.card_details = OracleOrgCreditCardDetails(
                card_number = self.card_number.data,
                expiration_date = self.expiration_date.data
            )
        cust.save()
        return cust

    def update(self):
        cust = OracleOrgCustomer(email_id=self.email_id.data)
        service = OracleOrgServices.objects.get(id=self.service.data)
        cust.first_name = self.first_name.data
        cust.last_name = self.last_name.data
        cust.phone_number = self.phone_number.data
        cust.subscription_type = self.subscription_type.data
        cust.start_date = datetime.strptime(self.start_date.data, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%Y")
        cust.due_date = datetime.strptime(self.due_date.data, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%Y")
        cust.service = service
        cust.payment_mode = self.payment_mode.data
        cust.product = OracleOrgPayment(
            payment_status=self.payment_status.data,
            is_paying_today=self.is_paying_today.data,
            payment_mode=self.payment_mode.data,
            due_payment=float(service.service_cost_per_month*subscription_type_dict[self.subscription_type.data]),
            payment_pending_days=self.payment_pending_days.data,
            is_defaulter=self.is_defaulter.data,
            transaction_id=None
        )
        cust.card_details = OracleOrgCreditCardDetails(
            card_number=self.card_number.data,
            expiration_date=self.expiration_date.data
        )
        cust.save()
        return cust


class AddOrganisationServiceForm(Form):
    service_name = StringField()
    service_cost_per_month = FloatField()
    is_offer_available = BooleanField()
    start_date = StringField()
    end_date = StringField()
    discount_percent = IntegerField()
    
    def validate(self):
        service_name=self.service_name.data
        if OracleOrgServices.objects.filter(service_name=service_name):
            return False, u"Service with this name Already exists"
        
    def save(self):
        service = OracleOrgServices(service_name=self.service_name.data)
        service.service_cost_per_month = float(self.service_cost_per_month.data)
        service.is_offer_available = self.is_offer_available.data
        if self.is_offer_available.data:
            service.discount_offers = OracleOrgAvailableOffer(
                is_offer_available = self.is_offer_available.data,
                start_date = datetime.strptime(self.start_date.data, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%Y"),
                end_date =  datetime.strptime(self.start_date.data, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%Y"),
                discount_percent = self.discount_percent.data
                
            )
        service.save()