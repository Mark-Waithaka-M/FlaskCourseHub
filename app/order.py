from flask import Blueprint,render_template,redirect,url_for,request
from .models import *
from flask_login import login_required,current_user

order = Blueprint('order',__name__)


@order.route('/order-details/<identifier>')
def order_details(identifier):
    order = Order.query.filter_by(identifier = identifier).first()
    return render_template('order-details.html',order=order)