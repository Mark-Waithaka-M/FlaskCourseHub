from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from . import db
from .models import *
from werkzeug.utils import secure_filename
import os


courseContent = Blueprint('courseContent',__name__)

@courseContent.route('/weekUpload', methods = ['POST', 'GET'])
def weekUpload():
    if request.method == 'POST':
        week_no = request.form['week_no']
        parent_course = request.form['course']
        

        new_week = Course_week( week_no=week_no, parent_course=parent_course)
        try:
            db.session.add(new_week)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('course-week.html')
        
        week = Course_week.query.filter_by(id = new_week.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('courseContent.courseContentUpload',id = week.id))
    
    return render_template('course-week.html')

@courseContent.route('/courseContentUpload', methods=['POST', 'GET'])
def courseContentUpload():
    if request.method == 'POST':
        parent_course = request.form['course']
        parent_week = request.form['week']
        heading = request.form['heading']

        new_content = Course_content(parent_course=parent_course, parent_week=parent_week, heading = heading)
        try:
            db.session.add(new_content)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('course-content.html')

        content = Course_content.query.filter_by(id = new_content.id).first()
        flash('item successfully added to db', category = 'success')
        return redirect(url_for('courseContent.videoUpload', id = content.id))
    
    return render_template('course-content.html')

@courseContent.route('/learningMaterialsUpload',methods = ['POST','GET']) 
def learningMaterialsUpload():
    if request.method == 'POST':
        parent_content = request.form['content']
        subheading = request.form['sub_heading']
        reading = request.form['reading']
        video = request.files['video']
        if video:
            mimetype = video.content_type

        new_material = Course_material(parent_content = parent_content,subheading=subheading,reading=reading,
            Video = secure_filename(video.filename)
            )
        video.save(os.path.join(current_app.config['UPLOAD_FOLDER'], video.filename))
        try:
            db.session.add(new_material)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('learningMaterials.html')
        
        material = Course_material.query.filter_by(id = new_material.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('courseContent.learningMaterialsUpload',id = material.id))
    
    return render_template('learningMaterials.html')

