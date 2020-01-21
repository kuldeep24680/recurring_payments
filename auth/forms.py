import datetime

from marshmallow import Schema, ValidationError, fields, validate, validates
from wtforms import SelectMultipleField, Form, StringField, BooleanField

from auth.utils import authenticate
from organisation.model import OracleOrgUser
from wtforms import validators as v


class LoginForm(Form):
    email_id = StringField()
    password = StringField()
    
    def validate(self):
        self.user_cache = authenticate(email_id=self.email_id.data, password=self.password.data)
        if self.user_cache is None:
            return False, "Please enter correct information. Note that password is case-sensitive."
        else:
            return True, ''


class RegistrationForm(Form):
    username = StringField()
    email_id = StringField()
    password = StringField()
    password2 = StringField()
    is_head_merchant = BooleanField()
    
    def validate(self):
        user = OracleOrgUser.objects.filter(email_id=self.email_id.data).first()
        if user is not None:
            return False, "Please use a different email"
        password = self.password.data
        password2 = self.password2.data
        if password != password2:
            return False, "Password and Repeat Password does not match"
        is_head_merchant = self.is_head_merchant.data
        if is_head_merchant:
            user = OracleOrgUser.objects.filter(is_head_merchant=is_head_merchant).first()
            if user:
                return False, "There can only be one Head Merchant"
        return True, ""
    
    def save(self):
        user = OracleOrgUser(email_id=self.email_id.data)
        user.username = self.username.data
        user.is_head_merchant = self.is_head_merchant.data
        user.set_password(self.password.data)
        user.created_at = datetime.datetime.now()
        user.is_admin = False
        user.save()
        
