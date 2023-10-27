from flask import Blueprint, render_template,redirect,flash,request,url_for,current_app
from werkzeug.security import generate_password_hash,check_password_hash
import time
from .models import *
from .import db
from flask_login import login_user,logout_user,login_required,current_user
import sqlite3
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
from . import mail

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['fname']
        lastname = request.form['lname']
        password = request.form['password']
        cPassword = request.form['cPassword']

        params = [email, firstname, lastname, password, cPassword]

        for param in params:
            if param == '':
                flash('all fields are required', category='danger')
                return redirect(url_for('home.homepage'))
            
        if password != cPassword:
            flash('Passwords do not match', category='danger')
            return redirect(url_for('home.homepage'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('user already exists.', category='danger')
            return redirect(url_for('home.homepage'))
        

      
        new_user = User(firstname=firstname,email=email, lastname=lastname, password = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user,remember=True)
        return redirect(url_for('home.homepage'))
    return render_template('sign-up.html')


    

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            flash('all fields are required', category='error')
            return render_template('homepage.html')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember = True)
                flash('You successfully logged in',category = 'success')
                return render_template('homepage.html')
            else:
                flash('Wrong password!', category='danger')
                return render_template('homepage.html')
            
        else:
            flash('user with that email does not exist', category='danger')
            return render_template('homepage.html')
    return render_template('homepage.html')

@auth.route('/logout')
def logout():
    logout_user()
    flash('you have successfully logged out', category ='warning')
    return redirect(url_for('home.homepage'))

@auth.route('/forgot-password', methods=['POST', 'GET'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']

        user = User.query.filter_by(id = User.id).first()
        if not user:
            flash('That email is not recognized', category='danger')
            return redirect('home.homepage')
        
        #email confirmation config
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(email,salt = 'password-reset')
        msg = Message('password reset')
        msg.recipients = [email]
        link = url_for('auth.confirm_password_reset', token= token, _external = True)
        msg.html = """<button><a href='{0}'>click {1} to reset your password</button>""".format(link,str(link)+str(token))
        mail.send(msg)
        flash('kindly click the link sent in the email provided to change your password', category='success')

        return render_template('forget-password.html')  
    return render_template('forget-password.html') 
    

@auth.route('/reset-password/<token>', methods = ['POST', 'GET'])
def confirm_password_reset(token):
    if request.method == 'POST':
        try:

            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            email = s.loads(token,salt = 'password-reset', max_age = 3600)

            password = request.form['password']
            cpassword = request.form['cpassword']

            if password != cpassword:
                flash('passwords dont match', category='danger')
                return render_template('reset-password.html')
            
            user = User.query.filter_by(id = User.id).first()
            if user:
                flash('password reset successful', category = 'success')
                user.password = generate_password_hash(password)
                db.session.commit()

            else:
                flash('No user with that email exists.', category='danger')
                return render_template('reset-password.html')
            
            return render_template('password-reset-success.html')
        except SignatureExpired:
            return 'token expired'
    return render_template('reset-password.html', token = token)


@auth.route('/edit-user-details',methods = ['POST','GET'])
@login_required
def edit_user_details():
    if request.method == 'POST':
        try:       
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            user_name = request.form['user_name']
            email = request.form['email']

            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_new_password = request.form['confirm_new_password']
        except:
            flash('all fields are required',category='danger')
            return redirect(url_for('account.accounts'))


        if new_password != confirm_new_password:
            flash('Confirm new password does not match!Please try again',category='danger')
            return redirect(url_for('account.accounts'))
        
        if check_password_hash(current_user.password,current_password) ==False:
            flash('Wrong account password!Please try again',category='danger')
            return redirect(url_for('account.accounts'))
        
        current_user.firstname = first_name
        current_user.lastname = last_name
        current_user.email = email
        current_user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('user data updated successfully',category='success')
        return redirect(url_for('account.accounts'))

        

        
        