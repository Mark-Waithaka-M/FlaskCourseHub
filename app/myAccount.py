from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from flask_login import login_required,current_user
from .models import *


account = Blueprint('account',__name__)

@account.route('/account',methods = ['POST','GET'])
@login_required
def accounts():
    all_billing_details = Billing_details.query.filter_by(account_user = current_user.id).all()
    billing_details = all_billing_details[len(all_billing_details) - 1]


    return render_template('my-account.html',billing_details=billing_details)

