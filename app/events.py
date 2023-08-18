from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
import os
from .models import *
from werkzeug.utils import secure_filename


events = Blueprint('events',__name__)

@events.route('/events',methods = ['POST','GET'])
def event():
    page = request.args.get('page',1,type=int)
    _events = Event.query.paginate(per_page=10,page = page)
    popular_events = Event.query.filter_by(is_popular  = True).order_by(Event.id.desc()).paginate(per_page=4,page=1)
    return render_template('events.html', events=_events,popular_events = popular_events.items)

@events.route('/eventDetails/<id>',methods = ['POST','GET'])
def eventDetails(id):
    event = Event.query.filter(Event.id == id).first()
    return render_template('events-details.html',event=event )

@events.route('/new-event',methods = ['POST','GET'])
def new_event():
    if request.method == 'POST':
        heading = request.form['heading']
        price= request.form['price']
        image = request.files['image']
        location = request.form['location']
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        attendance = request.form['attendance']

        try:
            is_popular = request.form['is-popular']
            if is_popular == 'on':
                is_popular = True
            else:
                is_popular = False
        except:
            is_popular = False

        try:
            isPaid = request.form['isPaid']
            if isPaid == 'on':

                isPaid = True
            else:
                isPaid = False
        except:
            isPaid = False

        try:
            hasExpired = request.form['hasExpired']
            if hasExpired == 'on':
                hasExpired = True
            else:
                hasExpired = False
        except:
            hasExpired = False

        new_event = Event(heading = heading,price=price,Image=secure_filename(image.filename),is_popular = is_popular,location=location,start_date=start_date,end_date=end_date,isPaid = isPaid,hasExpired=hasExpired,attendance=attendance)
        db.session.add(new_event)
        db.session.commit()
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
        flash('Event has been added successfully',category='success')
        return redirect(url_for('events.event_paragraph_upload',id = new_event.id))
    return render_template('new-event.html')


@events.route('/event-paragraph-upload/<int:id>',methods = ['POST','GET'])
def event_paragraph_upload(id):
    event = Event.query.filter_by(id=id).first()
    if request.method == 'POST':
        content = request.form['content']

        new_paragraph = Event_desc_paragraph(paragraph_content = content,parent_event=id)
        db.session.add(new_paragraph)
        db.session.commit()
        flash('Paragraph successfully added!',category = 'success')
        return redirect(url_for('events.event_paragraph_upload',id = id))
    return render_template('new-event-paragraph.html',event = event)


@events.route('/event-speaker-upload/<int:id>',methods = ['POST','GET'])
def new_event_speaker(id):
    event = Event.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        occupation = request.form['occupation']
        image = request.files['image']
        
        new_speaker = Event_speaker(name=name,Image=secure_filename(image.filename),occupation=occupation,parent_event = id)
        db.session.add(new_speaker)
        db.session.commit()
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))

        flash('Speaker added successfully',category='success')
        return redirect(url_for('events.new_event_speaker',id=id))
    return render_template('new-event-speaker.html',event=event)
        

    


