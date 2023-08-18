from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from flask_login import login_required,current_user
from .models import *
dashboard = Blueprint('dashboard',__name__)

@dashboard.route('/dashboard',methods = ['POST','GET'])
@login_required
def dashboards():
    return render_template('dashboard-home.html')


@dashboard.route('/my profile')
@login_required
def my_profile():
    return render_template('dashboard-profile.html')


@dashboard.route('/dashboard/enrolled-courses')
@login_required
def dashboard_enrolled_courses():
    return render_template('dashboard-enrolled-courses.html')

@dashboard.route('/dashboard/wishlist')
@login_required
def dashboard_wishlist():
    return render_template('dashboard-wishlist.html')


@dashboard.route('/dashboard/reviews')
@login_required
def dashboard_reviews():
    return render_template('dashboard-reviews.html')

@dashboard.route('/dashboard/orders')
@login_required
def dashboard_orders():
    return render_template('dashboard-orders.html')

@dashboard.route('/dashboard/courses')
@login_required
def dashboard_courses():
    courses = Course.query.all()
    return render_template('dashboard-courses.html',courses = courses)

@dashboard.route('/dashboard/categories')
@login_required
def dashboard_categories():
    categories = Category.query.all()
    return render_template('dashboard-categories.html',categories = categories)

@dashboard.route('/dashboard/instructors')
@login_required
def dashboard_instructors():
    instructors = Instructors.query.all()
    return render_template('dashboard-instructors.html',instructors=instructors)


@dashboard.route('/dashboard/shop')
@login_required
def dashboard_shop():
    return render_template('dashboard-shop.html',items = Shop_item.query.all())


@dashboard.route('/dashboard/shop-categories')
@login_required
def dashboard_shop_categories():
    return render_template('dashboard-shop-categories.html',categories =  Shop_category.query.all())

@dashboard.route('/dashboard/all-orders')
def dashboard_all_orders():
    return render_template('dashboard-all-orders.html',orders = Order.query.all())

@dashboard.route('/dashboard/event')
def dashboard_events():
    return render_template('dashboard-events.html',events = Event.query.all())

@dashboard.route('/dashboard/blogs')
def dashboard_blogs():
    return render_template('dashboard-blogs.html',blogs = Blog_post.query.all())

@dashboard.route('/dashboard/blog-categories')
def dashboard_blog_categories():
    return render_template('dashboard-blog-categories.html',categories = Blog_categories.query.all())


@dashboard.route('/dashboard/blog-creators')
def dashboard_blog_creators():
    return render_template('dashboard-blog-authors.html',authors = Blog_creators.query.all())

