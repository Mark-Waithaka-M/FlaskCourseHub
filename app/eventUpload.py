from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from . import db
from .models import *
from werkzeug.utils import secure_filename
import os
from flask_login import login_required


eventUpload = Blueprint('eventUpload',__name__)



@eventUpload.route('/newEventUpload',methods = ['POST','GET']) 
def newEventUpload():
    if request.method == 'POST':
        heading = request.form['heading']
        price = request.form['price']
        paragraph = request.form['paragraph']
        image = request.files['image']
        is_popular = request.form['is_popular']

        try:
            if is_popular == 'on':
                is_popular = True
                
            else:
                is_popular = False

        except:
            is_popular = False
        

        new_Event = Event(heading = heading,
            price=price,paragraph = paragraph,is_popular = is_popular,
            Image = secure_filename(image.filename)
            )
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
        try:
            db.session.add(new_Event)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('events-upload.html')
        
        event = Event.query.filter_by(id = new_Event.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('eventUpload.newEventDetails'))
    
    return render_template('events-upload.html')

@eventUpload.route('/delete-event/<string:heading>')
@login_required
def delete_event(heading):
    event = Event.query.filter_by(heading=heading).first()
    db.session.delete(event)
    db.session.commit()
    flash('Event has been successfully delete',category='success')
    return redirect(url_for('dashboard.dashboard_events'))


@eventUpload.route('/newEventDetails',methods = ['POST','GET']) 
def newEventDetails():
    if request.method == 'POST':
        location = request.form['location']
        parent_event = 1
        

        new_EventDetails = Event_details(location = location, parent_event=parent_event)
       
        try:
            db.session.add(new_EventDetails)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('events-details-upload.html')
        
        event_detail = Event_details.query.filter_by(id = new_EventDetails.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('eventUpload.newEventSpeaker',id = event_detail.id))
    
    return render_template('events-details-upload.html')


@eventUpload.route('/newEventSpeaker',methods = ['POST','GET']) 
def newEventSpeaker():
    if request.method == 'POST':
        occupation = request.form['occupation']
        name = request.form['name']
        image = request.files['image']
        parent_event = 1
        

        new_Speaker = Event_speaker(occupation = occupation,
            name=name,
            Image = secure_filename(image.filename)
            )
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
       
        try:
            db.session.add(new_Speaker)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('event-speakers-upload.html')
        
        event_speaker = Event_speaker.query.filter_by(id = new_Speaker.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('eventUpload.newEventUpload',id = event_speaker.id))
    
    return render_template('event-speakers-upload.html')

@eventUpload.route('/newEventComment/<int:id>',methods = ['POST','GET'])
def newEventComment(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']
        parent_event = id
        

        new_Comment = Event_comment(name = name,
            email=email,comment=comment,parent_event=parent_event
            )
       
        try:
            db.session.add(new_Comment)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('events-comments-upload.html')
        
        flash('item successfully added to db',category='success')
        return redirect(url_for('events.eventDetails',id = id))
    return redirect(url_for('events.eventDetails',id = id))

