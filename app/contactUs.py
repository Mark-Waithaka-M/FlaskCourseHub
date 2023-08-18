from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from . import db
from .models import *
import os


contactUs = Blueprint('contactUs',__name__)

@contactUs.route('/contactUs',methods = ['POST','GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        new_contactUs =Contact_us(
            name = name,email=email,message=message
        )
        try:
            db.session.add(new_contactUs)
            db.session.commit()
        except:
            db.rollback()
            flash('Error in upload,try again later',category = 'danger')
            return render_template('contact-us.html')
        
        contactUs = Contact_us.query.filter_by(id = new_contactUs.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('contactUs.homepage', id=contactUs.id))
    
    return render_template('contact-us.html')