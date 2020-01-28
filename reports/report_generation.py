import tempfile

from organisation.model import OracleOrgMonthlyGraduatedCustomers, OracleOrgCustomer
from  reports.report_definition.customer_report import PAYMENT_DICT
from reports.report_definition.graduate_customer_report import CUSTOMER_DICT
from reports.report_definition.offline_transaction_report import TRANSACTION_DICT
from reports.report_writer import xlsx_report_writer


def generate_customer_payment_report(today,customers):
    required_payments = list()
    if customers.count==0:
        return False, ""
    for customer in customers:
        payment_dict = dict()
        payment_dict["first_name"] = customer.first_name
        payment_dict["last_name"] = customer.last_name
        payment_dict["subscription_type"] = customer.subscription_type
        payment_dict["email_id"] = customer.email_id
        payment_dict["service_name"] = customer.service.service_name
        payment_dict["code"] = customer.service.code
        payment_dict["payment_status"] = "Paid" if customer.payment.payment_status else "Not Paid"
        payment_dict["payment_mode"] = customer.payment.payment_mode
        payment_dict["due_amount"] = customer.payment.due_payment
        payment_dict["payment_pending_days"] = customer.payment.payment_pending_days
        payment_dict["phone_number"] = customer.phone_number
        payment_dict["defaulter"] = "Yes" if customer.payment.is_defaulter else "No"

        required_payments.append(payment_dict)

    tmp_dir = tempfile.mkdtemp(prefix="payments")
    filename = "{}/payment_report_{}.xlsx".format(
         tmp_dir, today.date()
    )
    report_name = xlsx_report_writer(
        required_payments, PAYMENT_DICT, filename
    )
    return True, report_name


def generate_monthly_graduated_customer_report(start_date, end_date):
    """
    generates graduate monthly customer report
    :param start_date:
    :param end_date:
    :return: status,report
    """
    customers = OracleOrgMonthlyGraduatedCustomers.objects.filter(start_date__gte=start_date,due_date__lte=end_date)
    required_details = list()
    if customers.count==0:
        return False, ""
    for customer in customers:
        customer_dict = dict()
        customer_dict["first_name"] = customer.first_name
        customer_dict["last_name"] = customer.last_name
        customer_dict["subscription_type"] = customer.subscription_type
        customer_dict["email_id"] = customer.email_id
        customer_dict["service_name"] = customer.service_name
        customer_dict["service_code"] = customer.service_code
        customer_dict["payment_status"] = "Paid"
        customer_dict["payment_mode"] = customer.payment_mode
        customer_dict["paid_amount"] = customer.paid_amount
        customer_dict["start_date"] = customer.start_date.strftime("%d/%m/%Y")
        customer_dict["due_date"] = customer.due_date.strftime("%d/%m/%Y")
        customer_dict["phone_number"] = customer.phone_number
        
        required_details.append(customer_dict)
    tmp_dir = tempfile.mkdtemp(prefix="graduate_customer")
    filename = "{}/graduate_customer_report_{}_to_{}.xlsx".format(
        tmp_dir, start_date.date(), end_date.date()
    )
    report_name = xlsx_report_writer(required_details, CUSTOMER_DICT, filename)
    return True, report_name


def generate_offline_transaction_report(start_date, end_date):

    customers = OracleOrgCustomer.objects.filter(offline_transactions__transaction_date__gte=start_date,
                                                 offline_transactions__transaction_date__lte=end_date)

    required_transactions = list()
    if not customers:
        return False, ""
    for customer in customers:
        for transaction in customer.transactions_within_duration(start_date, end_date):
            transaction_dict = dict()
            transaction_dict["first_name"] = customer.first_name
            transaction_dict["last_name"] = customer.last_name
            transaction_dict["email_id"] = customer.email_id
            transaction_dict["phone_number"] = customer.phone_number
            transaction_dict["transaction_date"] = transaction.transaction_date
            transaction_dict["products"] = ','.join([str(product) for product in transaction.products])
            transaction_dict["paid_amount"] = transaction.paid_amount

            required_transactions.append(transaction_dict)

    tmp_dir = tempfile.mkdtemp(prefix="offline_transaction")
    filename = "{}/offline_transaction_report_{}_to_{}.xlsx".format(
        tmp_dir, start_date.date(), end_date.date()
    )
    report_name = xlsx_report_writer(
        required_transactions, TRANSACTION_DICT, filename
    )
    return True, report_name