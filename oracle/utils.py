import requests
from flask import request
from flask_mongoengine import Pagination
from oracle.settings import SANDBOX, KEY
from oracle.services import upload_to_s3_filename, get_presigned_url
from organisation.model import OracleOrgMonthlyGraduatedCustomers


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
    
    
def get_page_items():
    page = int(request.args.get("page", 1))
    per_page = request.args.get("per_page")
    if not per_page:
        per_page = 50
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def for_pagination(object_list):
    page, per_page, offset = get_page_items()
    if type(object_list) is list:
        count = len(object_list)
        a = offset
        b = offset + per_page
        object_list = object_list[a:b]
    else:
        count = object_list.count()
        object_list = object_list.skip(offset).limit(per_page)

    pagination = Pagination(
        iterable=object_list,
        page=page,
        per_page=per_page,
    )
    return pagination, object_list, offset


def monthly_graduate_customer_creation(customer):
    graduate_customer = OracleOrgMonthlyGraduatedCustomers(email_id=customer.email_id,
                                                           start_date = customer.start_date,
                                                           due_date = customer.due_date)
    graduate_customer.subscription_type = customer.subscription_type
    graduate_customer.first_name = customer.first_name
    graduate_customer.last_name = customer.last_name
    graduate_customer.service_name = customer.service.service_name
    graduate_customer.service_code = customer.service.code
    graduate_customer.paid_amount = customer.payment.due_payment
    graduate_customer.payment_status = "Paid"
    graduate_customer.payment_mode = customer.payment.payment_mode
    graduate_customer.phone_number = customer.phone_number
    graduate_customer.save()

    
    


