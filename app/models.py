from email.policy import default
from tkinter import CASCADE
from . import db
from sqlalchemy.sql import func
import datetime
from flask_login import UserMixin

user_course = db.Table('user_course',
                       db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                       db.Column('course_id',db.Integer,db.ForeignKey('course.id'))
                 )

course_materials = db.Table('course_materials',
                        db.Column('course_id',db.Integer,db.ForeignKey('course.id')),
                        db.Column('material_id',db.Integer,db.ForeignKey('materials.id'))
                )

course_instructor = db.Table('course_instructor',
                        db.Column('course_id',db.Integer,db.ForeignKey('course.id')),
                        db.Column('instructor_id',db.Integer,db.ForeignKey('instructors.id'))
                )




class Course(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(255),default = 'N/A')
    date_added = db.Column(db.DateTime,default = datetime.datetime.utcnow())
    duration = db.Column(db.String(55))
    lectures = db.Column(db.String(55))
    subject = db.Column(db.String(55))
    language = db.Column(db.String(55))
    Image = db.Column(db.String(255))
    category = db.Column(db.Integer,db.ForeignKey('category.id'),default = 1)
    level = db.Column(db.String(255))
    prerequisites = db.relationship('Prerequisite',backref = 'course',lazy = True,cascade = 'all,delete')
    about = db.relationship('About',backref = 'course',lazy = True,cascade = 'all,delete')
    objectives = db.relationship('Objectives',backref = 'course',lazy = True,cascade = 'all,delete')
    requirements = db.relationship('Requirements',backref = 'course',lazy = True,cascade = 'all,delete')
    reviews = db.relationship('Reviews',backref = 'course',lazy = True,cascade = 'all,delete')
    isPaid = db.Column(db.Boolean,default = True)
    wishlist_items = db.relationship('Wishlist',backref = 'course',lazy = True,cascade = 'all,delete')
    audiences = db.relationship('Audience',backref =  'course',lazy=True,cascade = 'all,delete')
    price_charters = db.relationship('Price_charter',backref = 'course',lazy=True,cascade='all,delete')
    course_materials = db.relationship('Materials',secondary='course_materials',backref = 'courses',cascade = 'all,delete')
    topics = db.relationship('Course_topics',backref = 'course',lazy=True,cascade='all,delete')
    instructors = db.relationship('Instructors',secondary='course_instructor',backref = 'courses',cascade = 'all,delete')
    course_orders = db.relationship('Course_purchase',backref = 'course',lazy= True)
    caption = db.Column(db.Text,default ='n/a')
    



    def price(self):
        latest_price = Price_charter.query.filter_by(id = self.id).all()
        try:
            price = latest_price[len(latest_price) - 1]
        except:
            price = '0'
        return price
    
class Course_purchase(db.Model):
    id = db.Column(db.Integer,primary_key= True,autoincrement=True)
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    name = db.Column(db.String,default='N/A')
    owner = db.Column(db.Integer,db.ForeignKey('user.id'))
    identifier = db.Column(db.String(45))
    date = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    price = db.Column(db.Integer)
    status = db.Column(db.String(25),default = 'processing')
    
class Materials(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.String(255),unique = True)

#------------------------------------------------------------------------------------------------#

class Course_topics(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    topic = db.Column(db.String(255),nullable = False)
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    topic_contents = db.relationship('Topic_content',backref='course',lazy = True,cascade = 'all,delete')

class Topic_content(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    title = db.Column(db.Text)
    type = db.Column(db.String(25))
    parent_topic = db.Column(db.Integer,db.ForeignKey('course_topics.id'))
    video = db.Column(db.String(255),nullable = True)
    mimetype = db.Column(db.Text,nullable =True)
    paragraphs = db.relationship('Topic_paragraphs',backref='topic_content',lazy=True,cascade='all,delete')

class Topic_paragraphs(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.Text)
    parent_topic_content = db.Column(db.Integer,db.ForeignKey('topic_content.id'))

#---------------------------------------------------------------------------------------------#
class Wishlist(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(255))
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    owner = db.Column(db.Integer,db.ForeignKey('user.id'))
    date = db.Column(db.DateTime,default = datetime.datetime.utcnow())
    image = db.Column(db.Text)

    
    

class Category(db.Model):
     id = db.Column(db.Integer,primary_key = True,autoincrement = True)
     course_category = db.Column(db.String(55))
     courses = db.relationship('Course',backref = 'categories',lazy = True,cascade = 'all,delete')
     image = db.Column(db.Text,default = 't.jpeg')

class Prerequisite(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    prerequisite_course = db.Column(db.Text)
    Image = db.Column(db.String(255))

class About(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.Text)
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    paragraphs = db.relationship('Paragraph',backref = 'about',cascade = 'all,delete')

    
      


class Paragraph(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    parent_about = db.Column(db.Integer,db.ForeignKey('about.id'))
    content = db.Column(db.Text)


class Objectives(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.String(255))
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))

class Requirements(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.String(255))
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))

class Audience(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.String(255))
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    

class Instructors(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(255))
    Image = db.Column(db.String(255))

    def students(self):
        student = 0
        for course in self.courses:
            student += course.enrolled_students 
        return student
    


class Instructor_reviews(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    parent_instructor = db.Column(db.Integer,db.ForeignKey('instructors.id'))



class Reviews(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    date_added = db.Column(db.DateTime,default = datetime.datetime.utcnow())
    content = db.Column(db.Text)
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))
    author = db.Column(db.Integer,db.ForeignKey('user.id'))



class Price_charter(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    cost = db.Column(db.Integer)
    discounted_price = db.Column(db.Integer)
    parent_course = db.Column(db.Integer,db.ForeignKey('course.id'))







#<-----------------------------------------------Authentication-------------------------------------------------------------->
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    user_name = db.Column(db.String(255),default='n/a')
    job_title = db.Column(db.String(255))
    bio = db.Column(db.Text)
    blog_comments = db.relationship('Blog_comment', backref='user', lazy=True, passive_deletes=True,cascade = 'all,delete')
    enrolled = db.relationship('Course',secondary='user_course',backref = 'enrolled_students',cascade = 'all,delete')
    wishlist_items = db.relationship('Wishlist',backref = 'user',lazy=True,cascade = 'all,delete')
    cart_items = db.relationship('Cart',backref='user',lazy=True,cascade='all,delete')
    is_admin = db.Column(db.Boolean(),default = False)
    billing_addresses = db.relationship('Billing_details',backref = 'user',lazy=True,cascade='all,delete')
    orders = db.relationship('Order',backref = 'user',lazy=True,cascade='all,delete')
    all_reviews = db.relationship('Reviews',backref='user',lazy=True,cascade='all,delete')
    course_purchases = db.relationship('Course_purchase',backref='account_user',lazy=True)
    

#<-----------------------------------------------BLOG-------------------------------------------------------------->


class Blog_categories(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    category_name = db.Column(db.String(100))
    blogs = db.relationship('Blog_post',backref='blog_category',lazy = True)

# Table for storing the blog posts
class Blog_post(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    Image = db.Column(db.String(255))
    category = db.Column(db.Integer,db.ForeignKey('blog_categories.id'))
    heading = db.Column(db.String(255))
    highlight = db.Column(db.Text)
    caption = db.Column(db.Text)
    blog_creator = db.Column(db.Integer, db.ForeignKey('blog_creators.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Blog_comment', backref='blog',lazy = True,cascade = 'all,delete')
    subheadings = db.relationship('Blog_heading',backref = 'blog',lazy =True,cascade = 'all,delete')
    paragraphs = db.relationship('Blog_paragraph',backref = 'post',lazy = True,cascade = 'all,delete')

class Blog_heading(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    heading = db.Column(db.Text)
    parent_blog = db.Column(db.Integer,db.ForeignKey('blog_post.id'))
    paragraphs = db.relationship('Blog_paragraph',backref = 'parent_heading',lazy = True,cascade = 'all,delete')

class Blog_paragraph(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.Text)
    parent_blog_heading = db.Column(db.Integer,db.ForeignKey('blog_heading.id'))
    parent_blog = db.Column(db.Integer,db.ForeignKey('blog_post.id'))

# Table for storing the blog creators
class Blog_creators(db.Model):
    __tablename__ = 'blog_creators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    Image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    blogs = db.relationship('Blog_post', backref='blog_creators',lazy = True,cascade = 'all,delete')





# Table for storing the blog comments
class Blog_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    blog_post = db.Column(db.Integer, db.ForeignKey('blog_post.id', ondelete="CASCADE"))

#<-----------------------------------------------BLOG-------------------------------------------------------------->


class Contact_us(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(70), nullable=False)
    message = db.Column(db.Text)


#<-----------------------------------------------BLOG-------------------------------------------------------------->

class Event(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(255), nullable=False)
    price= db.Column(db.Integer)
    paragraph = db.Column(db.Text)
    Image = db.Column(db.String(255))
    is_popular = db.Column(db.Boolean,default = False)
    location = db.Column(db.String(45))
    start_date = db.Column(db.String(45))
    end_date = db.Column(db.String(45))
    isPaid = db.Column(db.Boolean(),default = True)
    hasExpired = db.Column(db.Boolean,default = False)
    attendance = db.Column(db.Integer)
    event_speakers = db.relationship('Event_speaker',backref = 'event',lazy = True,cascade = 'all,delete')
    event_comments = db.relationship('Event_comment',backref = 'event',lazy = True,cascade = 'all,delete')
    paragraphs = db.relationship('Event_desc_paragraph',backref = 'course',lazy = True,cascade= 'all,delete')

class Event_desc_paragraph(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    paragraph_content = db.Column(db.Text)
    parent_event = db.Column(db.Integer,db.ForeignKey('event.id'))

class Event_speaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String(255))
    occupation = db.Column(db.String(255))
    name = db.Column(db.String(255))
    parent_event = db.Column(db.Integer,db.ForeignKey('event.id'))


class Event_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    comment = db.Column(db.Text)
    parent_event = db.Column(db.Integer,db.ForeignKey('event.id'))



#<-----------------------------------------------SHOP-------------------------------------------------------------->
class Shop_category(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    category_name = db.Column(db.String(45))
    shop_items = db.relationship('Shop_item',backref='shop_category',lazy=True,cascade='all,delete')

class Shop_item(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    name = db.Column(db.String(45))
    category = db.Column(db.Integer,db.ForeignKey('shop_category.id'))
    author = db.Column(db.String(255))
    caption = db.Column(db.Text)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer)
    sku = db.Column(db.String(255))
    image = db.Column(db.Text)
    language = db.Column(db.String(255))
    tags =  db.relationship('Shop_item_tag',backref='shop_item',lazy=True,cascade='all,delete')
    reviews = db.relationship('Shop_item_review',backref = 'shop_item',lazy=True,cascade='all,delete')
    cart_items = db.relationship('Cart',backref='cart_item_parent',lazy=True)
    prices = db.relationship('Shop_item_charter',backref='parent_shop_item',lazy=True,cascade='all,delete')
    order_items = db.relationship('Order_item',backref = 'parent_shop_item',lazy=True,cascade='all,delete')

    def price(self):
        try:
            return self.prices[len(self.prices) - 1].price
        except:
            return 0

class Shop_item_charter(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    parent_item = db.Column(db.Integer,db.ForeignKey('shop_item.id'))
    price = db.Column(db.Integer,default=0)

class Shop_item_tag(db.Model):
    id = db.Column(db.Integer,primary_key= True,autoincrement=True)
    tag_content = db.Column(db.String(25))
    parent_item = db.Column(db.Integer,db.ForeignKey('shop_item.id'))

class Shop_item_review(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    comment = db.Column(db.Text)
    image = db.Column(db.Text,default = 'default.jpg')
    time = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    parent_item = db.Column(db.Integer,db.ForeignKey('shop_item.id'))

#---------------------------------CART---------------------------------
class Cart(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    parent_product = db.Column(db.Integer,db.ForeignKey('shop_item.id'))
    quantity = db.Column(db.Integer,default=1)
    item_owner = db.Column(db.Integer,db.ForeignKey('user.id'))


class Partner(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    logo = db.Column(db.String(255))

#--------------------------Shipping details----------------------------------------
class Billing_details(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    company_name = db.Column(db.String(255),default = 'n/a')
    country = db.Column(db.String(255))
    street_address = db.Column(db.String(255))
    apartment = db.Column(db.String(255))
    town = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(255))
    account_user = db.Column(db.Integer,db.ForeignKey('user.id'))

#--------------------------------Order------------------------------------------------
class Order(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    identifier = db.Column(db.String(55))
    date = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    status = db.Column(db.String(55),default='processing')
    total = db.Column(db.Integer)
    account_user = db.Column(db.Integer,db.ForeignKey('user.id'))
    order_items = db.relationship('Order_item',backref='order',lazy=True,cascade='all,delete')


class Order_item(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    shop_product = db.Column(db.Integer,db.ForeignKey('shop_item.id'))
    parent_order = db.Column(db.Integer,db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer)