from flask import url_for, render_template, flash, request, Blueprint
from flask_login import current_user, login_user, login_required
from werkzeug.utils import redirect

from auth.forms import LoginForm, RegistrationForm
from dashboard.forms import AddOrganisationCustomerForm, AddOrganisationServiceForm
from oracle import mainapp
from organisation.model import OracleOrgMerchant, OracleOrgCustomer, OracleOrgServices
from oracle.tasks import subscription_assignment

dashboard_views = Blueprint("dashboard_views", __name__, template_folder="templates")



@dashboard_views.route('/login', methods=['GET', 'POST'])
def oracle_org_login():
    if request.method == "GET":
        return render_template('templates/forgot_password.html')
    
    if request.method == "POST":
        
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = OracleOrgMerchant.objects.filter(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            return redirect(url_for('index'))
        return render_template('templates/forgot_password.html', title='Sign In', form=form)
    
# @mainapp.route('/reset_password', method=['POST'])
# def reset_password():
#     email_id = request.args.get("email_id", "")
#     # token = user.get_reset_password_token()
#     # send_email_mailgun('Reset Your Password',
#     #            recipients=[email_id],
#     #            text_body=render_template('email/reset_password.txt',
#     #                                      user=user, token=token),
#     #            html_body=render_template('email/reset_password.html',
#     #                                      user=user, token=token))


@dashboard_views.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = OracleOrgMerchant(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@dashboard_views.route('/customer/new', methods=['POST'])
@login_required
def oracle_org_create_customer():
    if request.method == "POST":
        email_id = request.args.get("email_id", "")
        customer_form = AddOrganisationCustomerForm(request.form)
        status, msg = customer_form.validate()
        if status:
            customer_form.save()
            customer = OracleOrgCustomer.objects.get(email_id=email_id)
            subscription_assignment.delay(customer.id)
        else:
            flash(msg, "error")
            kwargs = locals()
        return redirect(
            url_for("dashboard_views.oracle_org_customers")
        )


@dashboard_views.route(
    "/customers/<customer_id>/update", methods=["GET", "POST", "DELETE"]
)
@login_required
def oracle_org_customer_update(customer_id):
    if request.method == "GET":
        customer = OracleOrgCustomer.objects.get(id=str(customer_id))
        service = OracleOrgServices.objects.filter()
        kwargs = locals()
        return render_template("customer_update.html", **kwargs)

    if request.method == "POST":
        form = AddOrganisationCustomerForm(request.form)
        form.update()
        kwargs = locals()
        return redirect(
            url_for("dashboard_views.oracle_org_customers")
        )
    if request.method == "DELETE":
        customer = OracleOrgCustomer.objects.get(id=str(customer_id))
        customer.delete()
        return redirect(
            url_for("dashboard_views.oracle_org_customers")
        )
        


@dashboard_views.route("/customers", methods=["GET"])
@login_required
def oracle_org_customers():
    if request.method == "GET":
        customers = OracleOrgCustomer.objects.filter()
        services = OracleOrgServices.objects.filter()
        kwargs = locals()
        return render_template("customer_list.html", **kwargs)
    

@dashboard_views.route('/service/new', methods=['POST'])
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
            url_for("dashboard_views.oracle_org_services")
        )
    

@dashboard_views.route("/services/<service_id>/update", methods=['GET','POST'])
@login_required
def oracle_org_update_service(service_id):
    if request.method == "GET":
        service = OracleOrgServices.objects.filter()
        kwargs = locals()
        return render_template("service_update.html", **kwargs)

    if request.method == "POST":
        form = AddOrganisationServiceForm(request.form)
        form.update()
        kwargs = locals()
        return redirect(
            url_for("dashboard_views.oracle_org_services")
        )
    
    
@dashboard_views.route("/services", methods=["GET"])
@login_required
def oracle_org_services():
    if request.method == "GET":
        services = OracleOrgServices.objects.filter()
        kwargs = locals()
        return render_template("services_list.html", **kwargs)