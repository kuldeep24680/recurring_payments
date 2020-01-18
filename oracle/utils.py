import bcrypt
import requests
from oracle.local_config import *
from oracle.services import upload_to_s3_filename, get_presigned_url


def generate_bcrypt_hash(raw_password):
    """
    generates the encrypted hash
    :param raw_password:
    :return: The Bcrypt hash
    """
    result = bcrypt.hashpw(str(raw_password).encode("utf-8"), bcrypt.gensalt())
    return result.decode("utf-8")


def send_email_mailgun(subject, template, recipient, cc_recipient=None):
    request_url = "https://api.mailgun.net/v2/{0}/messages".format(SANDBOX)
    request = requests.post(
        request_url,
        verify=False,
        auth=("api", KEY),
        data={
            "from": "no-reply@oraclepayments.com",
            "cc": cc_recipient,
            "to": recipient,
            "subject": subject,
            "text": template,
        },
    )
    return request


def send_attachment(file, report_subject, recipient):
    """
    Uploads file to S3 and  pre signed link in email to recipient
    :param file: File path of file to send in email as link
    :param report:  Report subject
    :param args:
    :param kwargs:
    :return:
    """
    upload_to_s3_filename(file, key=file)
    download_url = get_presigned_url(file, ExpiresIn=604800)
    body = "{} is available on {}".format(report_subject, download_url)
    subject = "{} Reports".format(report_subject)

    send_email_mailgun(subject, body, recipient)

