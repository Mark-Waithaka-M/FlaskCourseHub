from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os.path import join,dirname,realpath
from os import path
from flask_mail import Mail
from flask_login import LoginManager
import os


db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

basedir = os.path.abspath(os.path.dirname(__file__))



def create_app():
    app = Flask(__name__)
   

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Optimus99.@localhost:5432/edumall'
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)),'static/uploads/')
    app.config['SECRET_KEY'] ='edumall_mark'
    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MpqN4DjyCqXEqNd8PquwRJ2ajmwiu41RrEsR5LOkkMEixdejANTavcRe2bxRq0Yjm5wgm9ckK5bb7aJ4gLIVw4E00GCiYnYuE'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MpqN4DjyCqXEqNdq7QkFIhqlaWEkZRuNtsGRAP19eHYMLy2eCAQe7HsThJgrVhUw8TdYqZmwwGuav35uBBWTjGo00EcCyLkSm'

   
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)

  
    
    from .models import Course,\
        Category,Prerequisite,\
            About,Paragraph,\
            Objectives,Requirements,\
            Audience,Instructors,\
            Instructor_reviews,Reviews,User,Blog_creators,\
            Blog_post,Blog_comment,\
            Contact_us,Event,\
            Event_speaker,Event_comment

    @app.context_processor
    def inject_data():

        categories  = Category.query.all()
        
        return {'categories':categories}


          

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .home import home
    from .aboutUs import aboutUs
    from .blog import blog
    from .cart import cart
    from .checkout import checkout
    from .contactUs import contactUs
    from .course import course
    from .events import events
    from .myAccount import account
    from .shop import shop
    from .wishlist import wishlist
    from .zoom import zoom
    from .courseUpload import courseUpload
    from .BlogUpload import  BlogUpload
    from .auth import auth
    from .eventUpload import eventUpload
    from .shopUpload import shopUpload
    from .courseContent import courseContent
    from .dashboard import dashboard
    from .partner import partner
    from .order import order
    from .course_content import course_content

   


    app.register_blueprint(home,url_prefix = '/')
    app.register_blueprint(aboutUs,url_prefix = '/')
    app.register_blueprint(blog,url_prefix = '/')
    app.register_blueprint(cart,url_prefix = '/')
    app.register_blueprint(checkout,url_prefix = '/')
    app.register_blueprint(contactUs,url_prefix = '/')
    app.register_blueprint(course,url_prefix = '/')
    app.register_blueprint(events,url_prefix = '/')
    app.register_blueprint(account,url_prefix = '/')
    app.register_blueprint(shop,url_prefix = '/')
    app.register_blueprint(wishlist,url_prefix = '/')
    app.register_blueprint(zoom,url_prefix = '/')
    app.register_blueprint(courseUpload,url_prefix = '/')
    app.register_blueprint(BlogUpload,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')
    app.register_blueprint(eventUpload,url_prefix = '/')
    app.register_blueprint(shopUpload,url_prefix = '/')
    app.register_blueprint(courseContent,url_prefix = '/')
    app.register_blueprint(dashboard, url_prefix = '/')
    app.register_blueprint(partner,url_prefix = '/')
    app.register_blueprint(order,url_prefix='/')
    app.register_blueprint(course_content,url_prefix='/')
    


    return app