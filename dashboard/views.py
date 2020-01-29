import datetime

from flask import url_for, render_template, flash, request, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from auth.forms import LoginForm, RegistrationForm
from dashboard.forms import AddOrganisationCustomerForm, AddOrganisationServiceForm, AddOrganisationProductForm, \
    AddOrganisationCustomerOfflineTransactonForm
from oracle.utils import for_pagination
from organisation.model import OracleOrgUser, OracleOrgCustomer, OracleOrgServices, OracleOrgProducts
from dashboard.forms import subscription_type_list, boolean_type_list
from oracle.tasks import subscription_assignment, cancel_customer_subscription_service, \
    monthly_graduated_customer_report, offline_customer_transactions_report

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
    "/customers/<customer_id>/update", methods=["GET", "POST"]
)
@login_required
def oracle_org_customer_update(customer_id):
    
    if request.method == "GET":
        customer = OracleOrgCustomer.objects.get(id=str(customer_id))
        products = OracleOrgProducts.objects.filter()
        services = OracleOrgServices.objects.filter()
        subscription_type = subscription_type_list
        boolean_type = boolean_type_list
        kwargs = locals()
        return render_template("customer/customer_update.html", **kwargs)
    
    if request.method == "POST":
        form = AddOrganisationCustomerForm(request.form)
        cancel_subscription = bool(form.cancel_subscription.data)
        reassign_subscription = bool(form.reassign_subscription.data)
        cust = form.update()
        
        if cancel_subscription and cust.subscription_id is not None:
            cancel_customer_subscription_service.delay(str(cust.id))
        # reassignment if customer does not have a subscription id
        if reassign_subscription and not cust.subscription_id:
            subscription_assignment.delay(str(cust.id))
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


@auth_views.route(
    "/customers/<customer_id>/offline_transaction", methods=["POST"]
)
@login_required
def oracle_org_add_offine_transaction(customer_id):
    
    if request.method == "POST":
        form = AddOrganisationCustomerOfflineTransactonForm(request.form)
        form.save()

        kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_customers")
        )


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
    customers = OracleOrgCustomer.objects.filter(service=service)
    if customers.count==0:
        service.delete()
        return redirect(
            url_for("auth_views.oracle_org_services")
        )
    else:
        flash(f"Service {service.service_name} is currently being used by customers and therefore can't be deleted.")
        return redirect(
            url_for("auth_views.oracle_org_services")
        )


@auth_views.route("/services/<service_id>/update", methods=['GET', 'POST'])
@login_required
def oracle_org_update_service(service_id):
    if request.method == "GET":
        service = OracleOrgServices.objects.get(id=str(service_id))
        products = OracleOrgProducts.objects.filter()
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
        products = OracleOrgProducts.objects.filter()
        kwargs = locals()
        return render_template("services/service_creation.html", **kwargs)


@auth_views.route('/product/new', methods=['POST'])
@login_required
def oracle_org_create_product():
    if request.method == "POST":
        product = AddOrganisationProductForm(request.form)
        status, msg = product.validate()
        if status:
            product.save()
        else:
            flash(msg, "error")
            kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_products")
        )


@auth_views.route("/products/<product_id>/delete")
@login_required
def oracle_org_delete_product(product_id):
    product = OracleOrgProducts.objects.get(id=str(product_id))
    product.delete()
    return redirect(
        url_for("auth_views.oracle_org_products")
    )


@auth_views.route("/products/<product_id>/update", methods=['GET', 'POST'])
@login_required
def oracle_org_update_product(product_id):
    if request.method == "GET":
        product = OracleOrgProducts.objects.get(id=str(product_id))
        kwargs = locals()
        return render_template("products/product_update.html", **kwargs)
    
    if request.method == "POST":
        form = AddOrganisationServiceForm(request.form)
        form.save()
        kwargs = locals()
        return redirect(
            url_for("auth_views.oracle_org_products")
        )
    
    
@auth_views.route("/products", methods=["GET"])
@login_required
def oracle_org_products():
    if request.method == "GET":
        products = OracleOrgProducts.objects.filter()
        kwargs = locals()
        return render_template("products/product_creation.html", **kwargs)
    
    
@auth_views.route("/reports", methods=["GET", "POST"])
@login_required
def oracle_org_report_analysis():
    
    if request.method == "GET":
        user = OracleOrgUser.objects.get(id=current_user.id)
        kwargs = locals()
        return render_template("reports/reports.html", **kwargs)


@auth_views.route("/report/graduated_customer", methods=["POST"])
@login_required
def oracle_org_graduate_customer_report():

    if request.method == "POST":
        user = OracleOrgUser.objects.get(id=current_user.id)
        start_date = datetime.datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        monthly_graduated_customer_report(user.id,start_date,end_date)
        
        flash(
            "Report is being generated. It will be sent to your registered email Id {}.If this is not the correct email ID, please contact your administrator to update your email ID.".format(
                user.email_id
            ),
            "success",
        )
        return redirect(url_for("auth_views.oracle_org_report_analysis"))


@auth_views.route("/report/offline_transaction", methods=["POST"])
@login_required
def oracle_org_customer_offline_transaction_report():
    if request.method == "POST":
        user = OracleOrgUser.objects.get(id=current_user.id)
        start_date = datetime.datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        offline_customer_transactions_report(user.id, start_date, end_date)
        
        flash(
            "Report is being generated. It will be sent to your registered email Id {}.If this is not the correct email ID, please contact your administrator to update your email ID.".format(
                user.email_id
            ),
            "success",
        )
        return redirect(url_for("auth_views.oracle_org_report_analysis"))
        

