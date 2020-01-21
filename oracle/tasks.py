import datetime
import logging
from celery import Celery
from oracle import mainapp
from organisation.model import OracleOrgCustomer,OracleOrgUser
from oracle.utils import send_email_mailgun, send_attachment, monthly_graduate_customer_creation
from celery.task import periodic_task
from celery.schedules import crontab
from oracle.settings import BUFFER_PERIOD
from payment_modes.credit_card.create_subscription import create_subscription
from payment_modes.credit_card.delete_subscription import cancel_subscription
from payment_modes.credit_card.get_subscription_payment_details import get_recurring_payment_transaction_id
from reports.utils import generate_customer_payment_report, generate_monthly_graduated_customer_report

celery = Celery("oracle.tasks",backend=mainapp.config["result_backend"],broker=mainapp.config["celery_broker_url"])

celery.conf.update(mainapp.config)

logger = logging.getLogger(__name__)

def payment_confirmation_mail(merchant_email_id, customer_id):
    """
    fires notification mail to the respective customer.
    :param merchant_email_id:
    :param customer_id:
    :return:
    """
    customer = OracleOrgCustomer.objects.get(id=str(customer_id))
    start_date = customer.start_date.strftime("%d/%m/%Y")
    end_date = customer.due_date.strftime("%d/%m/%Y")
    body = f"Thanks for choosing our service {customer.service.service_name}! Amount {customer.payment.due_payment} has been charged for duration {start_date} to {end_date} via credit card payments.Look forward to serving you."
    header = "Payment Confirmation"
    send_email_mailgun(header, body, customer.email_id, merchant_email_id)


@celery.task
def subscription_assignment(customer_id):
    """
    assigns subscription IDs to the customers
    :param customer_id:
    :return:
    """
    customer = OracleOrgCustomer.objects.get(id=customer_id)
    kwargs = {
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "due_amount": customer.payment.due_payment,
        "number_days": int(customer.subscription_type)*30,
        "start_date": customer.start_date.strftime("%d/%m/%Y"),
        "card_number": customer.card_details.card_number,
        "expiration_date": customer.card_details.expiration_date
    }
    status, subscription_id = create_subscription(**kwargs)
    if status:
        customer.update(set__subscription_id=str(subscription_id))
        customer.update(set__was_subscribed=True)
        
        
@celery.task
def get_subscription_transaction_id(customer_id):
    "fetches the transactio_id for recurring payment through subscription ID "
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
    """
    Retry mechanism for subscription ID assignment to customers
    :return:
    """
    customers = OracleOrgCustomer.objects.filter(subscription_id=None, was_subscribed=False, is_active=True)
    if customers.count > 0:
        for customer in customers:
            subscription_assignment.delay(str(customer.id))


@periodic_task(run_every=crontab(minute=30, hour=16))
def fetch_recurring_payment_transaction_details():
    """
    Fetchs the transaction_id for recurring billing through subscription_id and notify customer via mail
    :return:
    """
    today_date = datetime.datetime.now().date().strftime("%d/%m/%Y")
    customers = OracleOrgCustomer.objects.filter(due_date=today_date, payment__payment_mode="subscription",is_active=True)
    if customers.count() > 0:
        for customer in customers:
            get_subscription_transaction_id.delay(str(customer.id))
    else:
        logger.info("No payments to made today")
        
        
@periodic_task(run_every=crontab(minute=30, hour=18))
def recurring_payment_merchant_notification():
    """
    sends recurring bill transaction report to the head merchant attached in a mail
    :return:
    """
    merchant = OracleOrgUser.objects.get(is_head_merchant=True)
    customers = OracleOrgCustomer.objects.filter(payment__is_paying_today=True,
                                                 payment__payment_pending_days__lte=BUFFER_PERIOD,
                                                 is_active=True)
    # code to generate the report
    today = datetime.datetime.now()
    if customers.count() > 0:
        status, report_name = generate_customer_payment_report(
            today, customers
        )
        graduated_customer = customers.filter(payment__payment_status=True)
        for customer in graduated_customer:
            monthly_graduate_customer_creation(customer)
            #reset stage
            type = int(customer.subscription_type)
            due_date = datetime.date.today() + datetime.timedelta(type * 365 / 12)
            customer.update(set__payment__is_paying_today=False)
            customer.update(set__payment__payment_pending_days=0)
            customer.update(set__start_date=today.date())
            customer.update(set__due_date=due_date.date())
        if status:
            send_attachment(report_name, f"Subscription Payment Report {today.date()}", merchant.email_id)
    

@periodic_task(run_every=crontab(minute=00, hour=19))
def defaultor_check_alert():
    """
    sends a detailed report of defaulter to the head merchant and marks matching customers as defaulter
    :return:
    """
    customers = OracleOrgCustomer.objects.filter(payment__is_paying_today=True,
                                                 payment__payment_pending_days__gte=BUFFER_PERIOD,
                                                 payment__is_defaulter=False,
                                                 is_active=True)
    merchant = OracleOrgUser.objects.get(is_head_merchant=True)
    today = datetime.datetime.now()
    if customers.count() > 0:
        for customer in customers:
            customer.update(set__payment__is_defaulter=True)
        
        status, report_name = generate_customer_payment_report(
            today, customers
        )
        if status:
            send_attachment(report_name, f"Payment Defaulter Report {today.date()}", merchant.email_id)
            
            
@celery.task
def cancel_customer_subscription_service(customer_id):
    cust = OracleOrgCustomer.objects.get(id=str(customer_id))
    subscription_id = cust.subscription_id
    if subscription_id:
        status = cancel_subscription(str(subscription_id))
        if status:
            cust.subscription_id = None
            cust.save()
            logger.info("Subscription for customer {} has been cancelled.".format(cust.email_id))
        else:
            logger.error("Subscription for customer {} could not be cancelled.".format(cust.email_id))
            
            
@celery.task
def monthly_graduated_customer_report(user_id, start_date, end_date):
    """
    This function is run both periodicly as well as invoked by celery to generate and mail  report attached.
    :param user_id:
    :param start_date:
    :param end_date:
    :return:
    """
    user = OracleOrgUser.objects.get(id=user_id)
    status, report_name = generate_monthly_graduated_customer_report(
        start_date, end_date)
    if status:
        send_attachment(report_name, "Graduate Customer Report", user.email_id)
    else:
        logger.error("Graduate Customer Report has not been generated.")
        
        
    
    
    
    
    
    
    
    
    
    
    
            


    