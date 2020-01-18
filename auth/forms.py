from marshmallow import Schema, ValidationError, fields, validate, validates

from organisation.model import OracleOrgMerchant


class NonEmptyStringField(fields.String):
    def _validate(self, value):
        if not value.strip() and self.required:
            raise ValidationError("Field cannot be empty.")
        return super(NonEmptyStringField, self)._validate(value)


class LoginForm(Schema):
    username = NonEmptyStringField(required=True)
    password = NonEmptyStringField(required=True)


class RegistrationForm(Schema):
    username = NonEmptyStringField(required=True)
    email = fields.String(email=True, required=True)
    password = NonEmptyStringField(required=True)
    password2 = NonEmptyStringField(required=True)
    
    def validate_username(self,username):
        user= OracleOrgMerchant.objects.filter(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        user = OracleOrgMerchant.objects.filter(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    def validate_password(self,password,password2):
        if password != password2:
            raise ValidationError('Password and Repeat Password does not match')