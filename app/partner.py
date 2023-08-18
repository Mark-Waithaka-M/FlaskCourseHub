from flask import render_template,redirect,url_for,request,current_app,Blueprint,flash
from .models import *
import os
from werkzeug.utils import secure_filename


partner = Blueprint('partner',__name__)


@partner.route('/new-partner',methods = ['POST','GET'])
def new_partner():
    if request.method == 'POST':
        logo = request.files['logo']

        new_partner = Partner(logo = secure_filename(logo.filename))

        try:
            db.session.add(new_partner)
            db.session.commit()
            logo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(logo.filename)))
            flash('new partner uploaded successfully',category = 'success')
            return redirect(url_for('partner.new_partner'))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('An error occurred during upload',category = 'danger')
            return redirect(url_for('partner.new_partner'))
    return render_template('new_partner.html')


