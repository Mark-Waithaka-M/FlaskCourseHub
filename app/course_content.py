from flask import Blueprint,render_template,redirect,url_for,flash,request,current_app
from werkzeug.utils import secure_filename
from .models import *
import os
course_content = Blueprint('course_content',__name__)

@course_content.route('/new-topic',methods = ['POST','GET'])
def new_topic():
    if request.method == 'POST':
        course = request.form['course']
        topic = request.form['topic']

        new_topic = Course_topics(parent_course=course,topic=topic)
        db.session.add(new_topic)
        db.session.commit()
        flash('New topic successfully added',category='success')
        return redirect(url_for('course_content.new_content_type',id = new_topic.id))
    return render_template('new-topic.html',courses = Course.query.all())

@course_content.route('/new-content-type/<int:id>',methods = ['POST','GET'])
def new_content_type(id):
    topic = Course_topics.query.filter_by(id=id).first()
    if request.method == 'POST':
        title = request.form['title'].lower()

        existing_content = Topic_content.query.filter_by(title = title).first()
        if existing_content:
            flash('That title already exists in another course,Please choose another title',category = 'danger')
            return redirect(url_for('course_content.new_content_type'))
        

        try:
            _type = request.form['type']
            if _type == 'reading':
                new_topic_content = Topic_content(type='reading',parent_topic=id,title = title)
                db.session.add(new_topic_content)
                db.session.commit()
                flash('add new paragraph for this reading',category='success')
                return redirect(url_for('course_content.new_reading_paragraph',id=new_topic_content.id))
            else:
                pass
        except:
            pass

        try:
            _type = request.form['type']
            if _type == 'video':
                new_topic_content = Topic_content(type='video',parent_topic = id,title = title)
                db.session.add(new_topic_content)
                db.session.commit()
                flash('add new content for this topic',category='success')
                return redirect(url_for('course_content.new_video',id = new_topic_content.id))
            else:
                pass
        except:
            pass
    return render_template('new-content-type.html',topic=topic)

@course_content.route('/new-reading-paragraph/<int:id>',methods = ['POST','GET'])
def new_reading_paragraph(id):
    content = Topic_content.query.filter_by(id=id).first()
    if request.method == 'POST':
        paragraph = request.form['content']
        
        new_paragraph = Topic_paragraphs(content=paragraph,parent_topic_content=id)
        db.session.add(new_paragraph)
        db.session.commit()
        flash('New paragraph added successfully,you can add a new one or click proceed to add a new topic content',category='success')
        return redirect(url_for('course_content.new_reading_paragraph',id=id))
    return render_template('new-reading-paragraph.html',content = content,topic = Course_topics.query.filter_by(id = content.parent_topic).first() )

@course_content.route('/new-video/<int:id>',methods = ['POST','GET'])
def new_video(id):
    content = Topic_content.query.filter_by(id = id).first()
    if request.method == 'POST':
        video = request.files['video']
        
        
        content.video = video.filename
        content.mimetype = video.mimetype
        db.session.commit()
        video.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(video.filename)))
        flash('New video has been uploaded successfully!You can now proceed to adding more content for this topic',category ='success')
        return redirect(url_for('course_content.new_content_type',id = content.course.id))
    return render_template('new-video.html',content = content)




        