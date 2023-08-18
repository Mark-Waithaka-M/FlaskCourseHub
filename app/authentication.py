from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from .models import *
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

authentication = Blueprint('authentication',__name__)

@authentication.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST': 
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('authentication.login'))

            else:
                flash('password is incorrect.', category='danger')

        else:
            flash('Email does not exist.', category='danger')

  
    return render_template('homepage.html',)

@authentication.route('/signUp', methods = ['POST','GET'])
def signUp():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='warning')
            return render_template('homepage.html')

        elif username_exists:
            flash('Username is already in use.', category='danger')
            return redirect(url_for('authentication.signUp'))

        elif password != confirmPassword:
            flash('password don\'t match', category = 'danger')

        elif len(username) < 2:
            flash('Username too short', category='danger')

        elif len(password) < 8:
            flash('Password should be at-least 8 characters', category='danger')

        elif len(email) < 4:
            flash('Email is invalid', category='danger')

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created', category = 'success')
            return redirect(url_for('authentication.signUp'))
   
    return render_template('homepage.html',)


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
   
    return render_template('homepage.html',)