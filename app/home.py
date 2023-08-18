from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from flask_login import login_required, current_user
from .models import *

home = Blueprint('home',__name__)

@home.route('/',methods = ['POST','GET'])
@home.route('/homepage')
def homepage():
    categories = Category.query.paginate(per_page = 5,page = 1)

    partners = Partner.query.paginate(per_page = 7,page = 1)

    return render_template('homepage.html',
                           categories = categories.items,
                           partners = partners.items
                           ) 