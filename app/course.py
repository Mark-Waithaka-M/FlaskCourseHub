from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from .models import *
from sqlalchemy import cast,Integer
from flask_login import login_required,current_user
import string
import stripe
import random

course = Blueprint('course',__name__)

@course.route('/course',methods = ['POST','GET'])
def courses():
    page = request.args.get('page',1,type=int)
    _courses = Course.query.paginate(per_page=10,page=page)
    return render_template('courses.html',
                           courses = _courses,
                           categories = Category.query.all()
                           )

@course.route('/course/search')
def course_search():
    page = request.args.get('page',1,type=int)
    q = request.args.get('q')
    courses = Course.query.filter(Course.name.like(f'%{q}%')).paginate(per_page = 10,page = page)
    return render_template('courses.html',courses = courses,categories = Category.query.all())

@course.route('/courseDetails/<name>',methods = ['POST','GET'])
def courseDetails(name):
    course = Course.query.filter(Course.name == name).first()
    _similar_courses = Course.query.filter_by(category = course.category).paginate(page=1,per_page=4)
    categories = Category.query.all()

   
    
    similar_courses = _similar_courses.items
    if course in similar_courses:
        similar_courses.remove(course)
    
   
    return render_template('course-details.html',course = course, similar_courses=similar_courses,categories = categories)

@course.route('/courseMaterials',methods = ['POST','GET'])
def courseMaterials():
    # course_materials = Course_content.query.filter(Course_content.id == id).first()
    return render_template('learning-materials.html')
    # return render_template('learning-materials.html', course_materials=course_materials)

@course.route('/courses/<string:category>')
def filter_by_category(category):
    cat = Category.query.filter_by(course_category = category ).first()
    courses = Course.query.filter_by(category = cat.id).all()
    return render_template('courses.html',
                           courses = courses,
                           categories = Category.query.all(),
                           name = category
                           )

@course.route('/courses-level/<string:level>')
def filter_by_level(level):
    courses = Course.query.filter_by(level = level.lower).all()
    return render_template('courses.html',
                           courses = courses,
                           name = level,
                           categories = Category.query.all(),
                           )

@course.route('/course-language/<string:language>')
def filter_by_language(language):
    courses = Course.query.filter(Course.language == language).all()
    return render_template('courses.html',
                           courses = courses,
                           name = language,
                           categories = Category.query.all(),
                           )

@course.route('/courses/paid')
def paid_courses():
    courses = Course.query.filter_by(isPaid = True).all()
    return render_template(
        'courses.html',
        courses = courses,
        name = 'paid',
        categories = Category.query.all()
    )

@course.route('/courses/free')
def free_courses():
    courses = Course.query.filter_by(isPaid = False).all()
    return render_template(
        'courses.html',
        courses = courses,
        name = 'free',
        categories = Category.query.all()
    )

@course.route('/course-duration/<string:duration>')
def filter_by_duration(duration):
    if duration == 'less than 7 hours':
        courses = Course.query.filter(cast(Course.duration,Integer) <= 7).all()
        name = 'less than7 hrs'
    elif duration == '7 - 10 hours':
        courses = Course.query.filter(cast(Course.duration,Integer) > 7 and cast(Course.duration,Integer) <= 10 ).all()
        name = '7 - 10hrs'
    elif duration == '10 - 15 hours':
        courses = Course.query.filter(cast(Course.duration,Integer) > 10 and cast(Course.duration,Integer) <= 15).all()
        name = '10 - 15 hours'
    elif duration == 'more than 15 hours':
        courses = Course.query.filter(cast(Course.duration,Integer) >= 15).all()
        name = 'more than 15 hours'

    return render_template('courses.html',
                           courses = courses,
                           name = name,
                           categories = Category.query.all()
                           )


@course.route('/enroll-course/<string:course_name>')
@login_required
def enroll_to_course(course_name):
    course = Course.query.filter_by(name = course_name).first()

    current_user.enrolled.append(course)
    db.session.commit()
    length = 4
    characters = string.digits
    identifier = ''.join(random.choice(characters) for i in range(length))
    new_course_purchase = Course_purchase(parent_course = course.id,name=course.name,owner = current_user.id,price = course.price_charters[len(course.price_charters) - 1].cost,identifier = identifier)
    db.session.add(new_course_purchase)
    db.session.commit()
    flash('You have successfully enrolled to course',category = 'success')
    return redirect(url_for('course.courseDetails',name = course_name))

@course.route('/unenroll-course/<string:course_name>')
@login_required
def unenroll_course(course_name):
    course = Course.query.filter_by(name = course_name).first()

    current_user.enrolled.remove(course)
    db.session.commit()
    flash('you have unenrolled from course',category = 'warning')
    return redirect(url_for('course.courses'))

@course.route('/attend-course/<string:name>')
def attend_course(name):
    course = Course.query.filter_by(name = name).first()
    content = course.topics[0].topic_contents[0]
    return redirect(url_for('course.render_content',name = content.title))

@course.route('/course-content/<string:name>')
def render_content(name):
    content = Topic_content.query.filter_by(title = name).first()
    course = Course.query.filter_by(name = content.course.course.name).first()
    return render_template('course-display.html',content = content,course = course)


@course.route('/pay-course/<string:name>')
@login_required
def course_checkout(name):

    course = Course.query.filter_by(name=name).first()
    image = str(url_for('static',filename = f'uploads/{course.Image}',_external = True))
    print(image)

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    session = stripe.checkout.Session.create(
        payment_method_types =['card'],
        line_items = [{
        'price_data':{
                         'currency':'usd',
                         'unit_amount':int(course.price_charters[len(course.price_charters) - 1].cost)  * 100,
                         'product_data':{
                                    'name':f'{course.name}',
                                    
                         }
        },
        'quantity':1,
        }],
        mode='payment',
        success_url = url_for('course.enroll_to_course',course_name = course.name,_external=True) + '?{CHECKOUT_SESSION_ID}',
        cancel_url = url_for('course.courseDetails',name=course.name,_external=True)

    )

    return {
        'checkout_session_id':session['id'],
        'checkout_public_key':current_app.config['STRIPE_PUBLIC_KEY']
    }
