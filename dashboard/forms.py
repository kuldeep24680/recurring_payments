import datetime

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

from organisation.model import OracleOrgCustomer, OracleOrgPayment, OracleOrgServices, OracleOrgCreditCardDetails


subscription_type_list = [
    {"id": '1', "value": "Monthly"},
    {"id": '3', "value": "Quarterly"},
    {"id": '6', "value": "Half Yearly"},
    {"id": '12', "value": "Yearly"},
]

boolean_type_list = [
    {"id": True, "value": "Yes"},
    {"id": False, "value": "No"},
]


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
    service_id = StringField()
    payment_mode = SelectField(
        choices=[("subscription", "Subscription Based"), ("cash", "Cash")]
    )
    card_number = StringField()
    expiration_date = StringField()
    cancel_subcription = BooleanField()
    payment_status = BooleanField()
    is_paying_today = BooleanField()
    payment_status = BooleanField()
    payment_pending_days = IntegerField()
    is_defaulter = BooleanField()
    is_active = BooleanField()

    def validate(self):
        
        email_id = self.email_id.data
        if OracleOrgCustomer.objects.filter(email_id=email_id):
            return False, "Product with this name Already exists"
        return True, ''

    def save(self, customer=None):
        if customer:
            cust = customer
        else:
            cust = OracleOrgCustomer(email_id=self.email_id.data)
        service = OracleOrgServices.objects.get(id=self.service_id.data)
        cust.first_name = self.first_name.data
        cust.last_name = self.last_name.data
        cust.phone_number = self.phone_number.data
        cust.subscription_type = self.subscription_type.data
        cust.start_date = datetime.datetime.strptime(self.start_date.data, '%Y-%m-%d').strftime("%d/%m/%Y")
        due_date = datetime.datetime.strptime(self.start_date.data, '%Y-%m-%d') + datetime.timedelta(int(self.subscription_type.data) * 365 / 12)
        cust.due_date = due_date.strftime("%d/%m/%Y")
        cust.service = service
        cust.payment_mode = self.payment_mode.data
        cust.created_at = datetime.datetime.now()
        cust.is_active = True
        cust.payment = OracleOrgPayment(
            payment_status = False,
            is_paying_today = False,
            payment_mode = self.payment_mode.data,
            due_payment = float(service.service_cost_per_month*(int(self.subscription_type.data))),
            payment_pending_days = 0,
            is_defaulter = False,
            transaction_id = None
        )
        if self.payment_mode.data == "subscription":
            cust.card_details = OracleOrgCreditCardDetails(
                card_number = self.card_number.data,
                expiration_date = self.expiration_date.data
            )
        cust.save()
        return cust

    def update(self):
        cust = OracleOrgCustomer.objects.get(email_id=self.email_id.data)
        service = OracleOrgServices.objects.get(id=self.service_id.data)
        cust.first_name = self.first_name.data
        cust.last_name = self.last_name.data
        cust.phone_number = self.phone_number.data
        cust.subscription_type = self.subscription_type.data
        cust.start_date = datetime.datetime.strptime(self.start_date.data, '%d/%m/%Y').strftime("%d/%m/%Y")
        due_date = datetime.datetime.strptime(self.start_date.data, '%d/%m/%Y') + datetime.timedelta(int(self.subscription_type.data) * 365 / 12)
        cust.due_date = due_date.strftime("%d/%m/%Y")
        cust.service = service
        cust.payment_mode = self.payment_mode.data
        cust.payment = OracleOrgPayment(
            payment_status=self.payment_status.data,
            is_paying_today=self.is_paying_today.data,
            payment_mode=self.payment_mode.data,
            due_payment=float(service.service_cost_per_month*(int(self.subscription_type.data))),
            payment_pending_days=self.payment_pending_days.data,
            is_defaulter=self.is_defaulter.data,
            transaction_id=None
        )
        cust.is_active = self.is_active.data
        cust.card_details = OracleOrgCreditCardDetails(
            card_number=self.card_number.data,
            expiration_date=self.expiration_date.data
        )
        cust.save()
        return cust


class AddOrganisationServiceForm(Form):
    service_name = StringField()
    code = StringField()
    service_cost = FloatField()
    is_offer_available = StringField()
    discount_percent = IntegerField()
    
    def validate(self):
        service_name=self.service_name.data
        if OracleOrgServices.objects.filter(service_name=service_name).first():
            return False, u"Service with this name Already exists"
        service_code = self.code.data
        if OracleOrgServices.objects.filter(code=service_code).first():
            return False, u"Service with this code Already exists"
        return True , ''
        
    def save(self):
        service = OracleOrgServices.objects.filter(service_name=self.service_name.data).first()
        if not service:
            service = OracleOrgServices(service_name=self.service_name.data)
        service.code = self.code.data
        service.service_cost_per_month = float(self.service_cost.data)
        service.created_at = datetime.datetime.now()
        service.is_offer_available = self.is_offer_available.data
        service.discount_percent = self.discount_percent.data
        service.save()