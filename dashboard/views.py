from flask import url_for, render_template, flash, request, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from auth.forms import LoginForm, RegistrationForm
from dashboard.forms import AddOrganisationCustomerForm, AddOrganisationServiceForm
from oracle.utils import for_pagination
from organisation.model import OracleOrgUser, OracleOrgCustomer, OracleOrgServices
from dashboard.forms import subscription_type_list, boolean_type_list
from oracle.tasks import subscription_assignment, cancel_customer_subscription_service
from payment_modes.credit_card.delete_subscription import cancel_subscription

auth_views = Blueprint("auth_views", __name__, template_folder="templates")


@auth_views.route('/', methods=['GET', 'POST'])
def oracle_org_login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_views.oracle_org_dashboard'))
    
    if request.method == "POST":
        
        form = LoginForm(request.form)
        status, message = form.validate()
        if status:
            login_user(form.user_cache, True)
            return redirect(url_for('auth_views.oracle_org_dashboard'))
        else:
            flash(message, "error")
    kwargs = locals()
    return render_template("auth/login.html", **kwargs)


@auth_views.route("/logout")
@login_required
def oracle_org_logout():
    logout_user()
    return redirect("/")


@auth_views.route('/dashboard', methods=['GET'])
@login_required
def oracle_org_dashboard():
    kwargs = locals()
    return render_template("dashboard.html", **kwargs)


@auth_views.route('/signup', methods=['GET', 'POST'])
def oracle_org_register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_views.oracle_org_login'))
    if request.method == "POST":
        form = RegistrationForm(request.form)
        status, message = form.validate()
        if status:
            form.save()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth_views.oracle_org_login'))
        else:
            flash(message, "error")
    
    kwargs = locals()
    return render_template("auth/register.html", **kwargs)


@auth_views.route('/customer/new', methods=['POST'])
@login_required
def oracle_org_create_customer():
    if request.method == "POST":
        
        email_id = request.args.get("email_id", "")
        customer_form = AddOrganisationCustomerForm(request.form)
        email_id = customer_form.email_id.data
        status, msg = customer_form.validate()
        if status:
            customer_form.save()
            customer = OracleOrgCustomer.objects.get(email_id=email_id)
            subscription_assignment.delay(str(customer.id))
        else:
            flash(msg, "error")
        kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_customers")
        )


@auth_views.route(
    "/customers/<customer_id>/delete")
@login_required
def oracle_org_delete_customer(customer_id):
    customer = OracleOrgCustomer.objects.get(id=str(customer_id))
    customer.delete()
    return redirect(
        url_for("auth_views.oracle_org_customers")
    )
    

@auth_views.route(
    "/customers/<customer_id>/update", methods=["GET", "POST", "DELETE"]
)
@login_required
def oracle_org_customer_update(customer_id):
    
    if request.method == "GET":
        customer = OracleOrgCustomer.objects.get(id=str(customer_id))
        services = OracleOrgServices.objects.filter()
        subscription_type = subscription_type_list
        boolean_type = boolean_type_list
        kwargs = locals()
        return render_template("customer/customer_update.html", **kwargs)
    
    if request.method == "POST":
        form = AddOrganisationCustomerForm(request.form)
        cancel_subscription = form.cancel_subcription.data
        cust = form.update()
        
        if cancel_subscription:
            cancel_customer_subscription_service.delay(str(cust.id))
        kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_customers")
        )



@auth_views.route("/customers", methods=["GET"])
@login_required
def oracle_org_customers():
    if request.method == "GET":
        customers = OracleOrgCustomer.objects.filter()
        services = OracleOrgServices.objects.filter()
        pagination1, products, offset1 = for_pagination(customers)
        kwargs = locals()
        return render_template("customer/customer_creation.html", **kwargs)


@auth_views.route('/service/new', methods=['POST'])
@login_required
def oracle_org_create_service():
    if request.method == "POST":
        service = AddOrganisationServiceForm(request.form)
        status, msg = service.validate()
        if status:
            service.save()
        else:
            flash(msg, "error")
            kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_services")
        )


@auth_views.route(
    "/services/<service_id>/delete")
@login_required
def oracle_org_delete_service(service_id):
    service = OracleOrgServices.objects.get(id=str(service_id))
    service.delete()
    return redirect(
        url_for("auth_views.oracle_org_services")
    )


@auth_views.route("/services/<service_id>/update", methods=['GET', 'POST'])
@login_required
def oracle_org_update_service(service_id):
    if request.method == "GET":
        service = OracleOrgServices.objects.get(id=str(service_id))
        boolean_type = boolean_type_list
        kwargs = locals()
        return render_template("services/service_update.html", **kwargs)
    
    if request.method == "POST":
        form = AddOrganisationServiceForm(request.form)
        form.save()
        kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_services")
        )


@auth_views.route("/services", methods=["GET"])
@login_required
def oracle_org_services():
    if request.method == "GET":
        services = OracleOrgServices.objects.filter()
        kwargs = locals()
        return render_template("services/service_creation.html", **kwargs)
