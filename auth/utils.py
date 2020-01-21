from organisation.model import OracleOrgUser


def authenticate(email_id=None, password=None):
    user = OracleOrgUser.objects(email_id=email_id).first()
    if user and password and user.check_password(password):
        return user
    return None
