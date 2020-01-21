import tempfile
from  reports.report_definition.customer_report import PAYMENT_DICT
from reports.report_generation import xlsx_report_writer


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