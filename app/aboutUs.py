from flask import Blueprint,render_template,redirect,request,url_for,flash,abort

aboutUs = Blueprint('aboutUs',__name__)

@aboutUs.route('/aboutUs',methods = ['POST','GET'])
def about():
    return render_template('about-us.html')