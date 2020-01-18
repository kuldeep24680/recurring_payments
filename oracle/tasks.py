import datetime

from flask_login import current_user

from oracle import celery
from organisation.model import OracleOrgCustomer,OracleOrgUser
from oracle.utils import send_email_mailgun, send_attachment
from celery.task import periodic_task
from celery.schedules import crontab
from oracle.local_config import BUFFER_PERIOD
from payment_modes.credit_card.create_subscription import create_subscription
from payment_modes.credit_card.get_subscription_payment_details import get_recurring_payment_transaction_id
from reports.utils import generate_customer_payment_report
import logging

logger = logging.getLogger(__name__)




def payment_confirmation_mail(merchant_email_id, customer_id):
    customer = OracleOrgCustomer.objects.get(id=customer_id)
    start_date = customer.start_date.strftime("%d/%m/%Y")
    end_date = customer.due_date.strftime("%d/%m/%Y")
    body = f"Thanks for choosing our service {customer.service.service_name}! Amount {customer.payment.due_payment} has been charged for duration {start_date} to {end_date} via credit card payments.Look forward to serving you."
    header = "Payment Confirmation"
    send_email_mailgun(header, body, customer.email, merchant_email_id)


@celery.task
def subscription_assignment(customer_id):
    customer = OracleOrgCustomer.objects.get(id=customer_id)
    kwargs = {
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "due_amount": customer.payment.due_payment,
        "number_days": int(customer.subscription_type*30),
        "start_date": customer.start_date,
        "card_number": customer.card_details.card_number,
        "expiration_date": customer.card_details.expiration_date
    }
    status, subscription_id = create_subscription(**kwargs)
    if status:
        customer.update(set__subscription_id=subscription_id)
        
        
@celery.task
def get_subscription_transaction_id(customer_id):
    customer = OracleOrgCustomer.objects.get(id=customer_id)
    merchant = OracleOrgUser.objects.get(is_head_merchant=True)
    customer.update(set__is_paying_today = True)
    status, transaction_id = get_recurring_payment_transaction_id(customer.subscription_id)
    if status:
        customer.update(set__payment__payment_status=True)
        customer.update(set__payment__transaction_id=transaction_id)
        payment_confirmation_mail(merchant.email_id, customer.id)
        
    else:
        days_cnt = customer.payment_pending_days + 1
        customer.update(set__payment__payment_status=False)
        customer.update(set__payment__payment_pending_days=days_cnt)
        
        
@periodic_task(run_every=crontab(minute=45, hour=20))
def subscription_assignment_retry_mechanism():
    customers = OracleOrgCustomer.objects.filter(subscription_id=None)
    if customers.count > 0:
        for customer in customers:
            subscription_assignment.delay(customer.id)


@periodic_task(run_every=crontab(minute=30, hour=16))
def fetch_recurring_payment_transaction_details():
    user = OracleOrgUser.objects.get(id=current_user.id)
    today_date = datetime.datetime.now().date().strftime("%d/%m/%Y")
    customers = OracleOrgCustomer.objects.filter(due_date=today_date, payment__payment_mode="subscription")
    if customers.count() > 0:
        for customer in customers:
            get_subscription_transaction_id.delay(customer.id)
    else:
        logger.info("No payments to made today")
        
        
@periodic_task(run_every=crontab(minute=30, hour=18))
def recurring_payment_merchant_notification():
    merchant = OracleOrgUser.objects.get(is_head_merchant=True)
    customers = OracleOrgCustomer.objects.filter(payment__is_paying_today=True,
                                                 payment__payment_pending_days__lte=BUFFER_PERIOD)
    # code to generate the report
    today = datetime.datetime.now()
    if customers.count() > 0:
        status, report_name = generate_customer_payment_report(
            today, customers
        )
        graduated_customer = customers.filter(payment__payment_status=True)
        for customer in graduated_customer:
            type = customer.subscription_type
            customer.update(set__payment__is_paying_today=False)
            customer.update(set__payment_pending_days=0)
            customer.update(set__start_date=today)
            customer.update(set__end_date=datetime.date.today() + datetime.timedelta(type * 365 / 12))
        if status:
            send_attachment(report_name, f"Subscription Payment Report {today.date()}", merchant.email)
    

@periodic_task(run_every=crontab(minute=00, hour=19))
def defaultor_check_alert():
    customers = OracleOrgCustomer.objects.filter(payment__is_paying_today=True,
                                                 payment__payment_pending_days=BUFFER_PERIOD,
                                                 payment__is_defaulter=False)
    merchant = OracleOrgUser.objects.get(is_head_merchant=True)
    today = datetime.datetime.now()
    if customers.count() > 0:
        for customer in customers:
            customer.set(set__is_defaulter=True)
        
        status, report_name = generate_customer_payment_report(
            today, customers
        )
        if status:
            send_attachment(report_name, f"Payment Defaulter Report {today.date()}", merchant.email)
            
    
    
        
        
    
    
    
    
    
    
    
    
    
    
    
            


    