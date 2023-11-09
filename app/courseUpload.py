from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from . import db
from .models import *
from werkzeug.utils import secure_filename
import os
from flask_login import login_required,current_user

courseUpload = Blueprint('courseUpload',__name__)



@courseUpload.route('/newUpload',methods = ['POST','GET']) 
def newUpload():
    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']
        duration = request.form['duration']
        lectures = request.form['lectures']
        subject = request.form['subject']
        language = request.form['language']
        image = request.files['image']
        category = request.form['category'] 

        existing_course = Course.query.filter_by(name = name).first()
        if existing_course:
            flash('this course already exists',category = 'danger')
            return redirect(url_for('courseUpload.newUpload'))
        

        new_Course = Course(name = name,
            level=level,duration = duration,
            lectures = lectures,subject = subject,language = language,category=category,
            Image = secure_filename(image.filename)
            )
       
        try:
            db.session.add(new_Course)
            db.session.commit()
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('new-course.html')
        
        flash('item successfully added to db',category='success')
        return redirect(url_for('courseUpload.prerequisitesUpload',id = new_Course.id))
    
    return render_template('new-course.html',categories = Category.query.all())

@courseUpload.route('/delete-course/<string:name>')
@login_required
def delete_course(name):
    course = Course.query.filter_by(name = name).first()
    db.session.delete(course)
    db.session.commit()
    flash('Course has been successfully deleted!',category='success')
    return redirect(url_for('dashboard.dashboard_courses'))



@courseUpload.route('/categoryUpload', methods= ['POST', 'GET'])
def categoryUpload():
    if request.method == 'POST':
        course_category = request.form['course_category']
        image = request.files['image']



        new_category = Category(course_category=course_category,image=secure_filename(image.filename))
        try:
            db.session.add(new_category)
            db.session.commit()
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))

        except:
            flash('Error in upload, try again later', category='danger')
            return render_template('new-course-category.html')
        
        new_category = Category.query.filter_by(id=new_category.id).first()
        flash('item successfully added to db', category='success')
        return redirect(url_for('dashboard.dashboard_categories'))
    
    return  render_template('new-course-category.html')

@courseUpload.route('/delete-category/<int:id>')
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    flash('Category delete successfully',category='success')
    return redirect(url_for('dashboard.dashboard_categories'))


@courseUpload.route('/prerequisitesUpload/<int:id>',methods = ['POST','GET'])
def prerequisitesUpload(id):
    if request.method =='POST':
        prerequisite_course_name = request.form['course_name']

        course = Course.query.filter_by(name=prerequisite_course_name).first()

        new_prerequisite = Prerequisite(parent_course=id,prerequisite_course=course.name,Image=course.Image)
        
        db.session.add(new_prerequisite)
        db.session.commit()
        flash('prerequisite added successfully',category = 'success')
        return redirect(url_for('courseUpload.prerequisitesUpload',id = id))
    else:
        return render_template('new-prerequisite.html',
                               course = Course.query.filter_by(id=id).first(),
                               courses = Course.query.all()
                               )
   



@courseUpload.route('/paragraphsUpload/<int:id>',methods = ['POST','GET'])
def paragraphsUpload(id):
    course = Course.query.filter_by(id=id).first()
    if request.method == 'POST':


        content = request.form['content']

        about = About.query.filter_by(parent_course=course.id).first()
        if about != None:
            try:
                new_paragraph = Paragraph(parent_about=about.id,content=content)
                db.session.add(new_paragraph)
                db.session.commit()
            except Exception as e:  
                print(e)
                flash('Error in upload, try again later', category='danger')
                return render_template('paragraphs.html')
        else:
            new_about = About(name=course.name,parent_course=course.id)
            db.session.add(new_about)
            db.session.commit()

            try:
                new_paragraph = Paragraph(parent_about=new_about.id,content=content)
                db.session.add(new_paragraph)
                db.session.commit()
            except Exception as e:  
                print(e)
                flash('Error in upload, try again later', category='danger')
                return render_template('paragraphs.html')
        flash('item successfully added to db,click proceed to add the next item.',category='success')
        return redirect(url_for('courseUpload.paragraphsUpload',id=id))
    return render_template('paragraphs.html',course = course)

@courseUpload.route('/objectivesUpload/<int:id>',methods = ['POST','GET'])
def objectivesUpload(id):
    course = Course.query.filter_by(id=id).first()
    if request.method == 'POST':
        objective = request.form['objective']
        
        new_objectives = Objectives(content = objective, parent_course = id)
        try:
            db.session.add(new_objectives)
            db.session.commit()
        except:
            flash('Error in upload, try again later', category='danger')
            return render_template('course-objectives.html',course = course)

        flash('objective successfully added,click proceed to proceed to adding th next item',category='success')
        return redirect(url_for('courseUpload.objectivesUpload',id=id))
        
    return render_template('course-objectives.html',course = course)


@courseUpload.route('/requirementsUpload/<int:id>',methods = ['POST','GET'])
def requirementsUpload(id):
    course = Course.query.filter_by(id=id).first()
    if request.method == 'POST':
        content = request.form['requirement']
        
        new_requirements = Requirements(content = content, parent_course = id)
        try:
            db.session.add(new_requirements)
            db.session.commit()
        except:
            flash('Error in upload, try again later', category='danger')
            return render_template('course-requirements.html',courses = Course.query.all())

        flash('Course requirement successfully added,click proceed to proceed to adding the next course item',category='success')
        return redirect(url_for('courseUpload.requirementsUpload',id = id))
        
    return render_template('course-requirements.html',course = course)

@courseUpload.route('/audienceUpload/<int:id>',methods = ['POST','GET'])
def audienceUpload(id):
    course = Course.query.filter_by(id =id).first()
    if request.method == 'POST':
        content = request.form['audience']
       
        
        new_audience = Audience(content = content, parent_course = id)
        try:
            db.session.add(new_audience)
            db.session.commit()
        except:
            flash('Error in upload, try again later', category='danger')
            return render_template('course-audience.html')

        flash('course audience added successfully,please clock proceed to proceed to adding the next course item',category='success')
        return redirect(url_for('courseUpload.audienceUpload',id=id))
        
    return render_template('course-audience.html',course=course)

@courseUpload.route('/priceUpload/<int:id>',methods = ['POST','GET'])
def priceUpload(id):
    course = Course.query.filter_by(id=id).first()
    if request.method == 'POST':
        original_price = request.form['cost']
        price_with_discount = request.form['discounted-price']

        new_price = Price_charter(cost=original_price,discounted_price=price_with_discount,parent_course=id)
        try:
            db.session.add(new_price)
            db.session.commit()
        except Exception as e:
            flash('Error in upload, try again later', category='danger')
            return render_template('course-charter.html')
        
        flash('course price added successfully,please clock proceed to proceed to adding the next course item',category='success')
        return redirect(url_for('courseUpload.priceUpload',id=id))
    return render_template('course-charter.html',course=course)
    




  








@courseUpload.route('/instructorUpload', methods = ['POST', 'GET'])
def instructorUpload():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']

        new_instructor = Instructors(
            name=name,
            Image = secure_filename(image.filename)
            )
        try:
            db.session.add(new_instructor)
            db.session.commit()
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('new-instructor.html')
        
        instructor = Instructors.query.filter_by(id = new_instructor.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('dashboard.dashboard_instructors'))
    
    return render_template('new-instructor.html')
@courseUpload.route('/delete-instructor/<int:id>')
def delete_instructor(id):
    instructor = Instructors.query.filter(Instructors.id==id).first()
    db.session.delete(instructor)
    db.session.commit()
    flash('Instructor deleted successfully',category='success')
    return redirect(url_for('dashboard.dashboard_instructors'))


@courseUpload.route('/instructorReview', methods = ['POST', 'GET'])
def instructorReview():
    if request.method == 'POST':
        parent_instructor = request.form['instructor']
       

        new_instructor_review = Instructor_reviews(parent_instructor=parent_instructor)

        try:
            db.session.add(new_instructor_review)
            db.session.commit()

        except:
            flash('Error in upload, try again later', category='danger')
            return redirect(url_for('courseUpload.newCourseInstructor'))
        
    return render_template('course-reviews.html')

@courseUpload.route('/newCourseInstructor', methods = ['POST', 'GET'])
def newCourseInstructor():
    if request.method == 'POST':
        course_id = request.form['course']
        instructor_id = request.form['instructor']
       

        new_course_instructor = Course_instructor(course_id=course_id, instructor_id=instructor_id)

        try:
            db.session.add(new_course_instructor)
            db.session.commit()

        except:
            flash('Error in upload, try again later', category='danger')
            return redirect(url_for('courseUpload.reviewsUpload'))
    
    return render_template('course-reviews.html')

@courseUpload.route('/reviewsUpload/<int:id>', methods = ['POST', 'GET'])
@login_required
def reviewsUpload(id):
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        email = request.form['email']
       

        new_review = Reviews(name=name,email=email, content=content,parent_course=id,author=current_user.id)
        try:
            db.session.add(new_review)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('course-reviews.html')
        course = Course.query.filter_by(id = id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('course.courseDetails',name =course.name ))
    
    return render_template('course-reviews.html')
