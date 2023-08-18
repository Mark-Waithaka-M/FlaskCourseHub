from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from .models import *

blog = Blueprint('blog',__name__)

@blog.route('/blog',methods = ['POST','GET'])
def blogs():
    _blogs = Blog_post.query.all()

    latest_blogs = Blog_post.query.order_by(Blog_post.id.desc()).paginate(per_page=4,page =1)
    if blog in latest_blogs.items:
        latest_blogs.items.remove(blog)


    return render_template('blog.html', blogs=_blogs,
                           latest_blogs = latest_blogs,
                           categories =  Blog_categories.query.all() 
                           )

@blog.route('/blogDetails/<id>',methods = ['POST','GET'])
def blogDetails(id):
    blog = Blog_post.query.filter(Blog_post.id == id).first()

    related_posts = Blog_post.query.filter_by(category = blog.category).paginate(page = 1,per_page = 4)
    if blog in related_posts.items:
        related_posts.items.remove(blog)

    barner_posts = []
    if Blog_post.query.count() < 3:
        pass
    else:
        barner_posts = Blog_post.query.paginate(per_page =3 ,page = 1)

        if blog in barner_posts.items:
            barner_posts.items.remove(blog)


    latest_blogs = Blog_post.query.order_by(Blog_post.id.desc()).paginate(per_page=4,page =1)
    if blog in latest_blogs.items:
        latest_blogs.items.remove(blog)




    return render_template('blog-details.html',
                           blog=blog,
                           related_posts = related_posts,
                           barner_posts=barner_posts,
                           latest_blogs = latest_blogs,
                           categories = Blog_categories.query.all()
                           )

@blog.route('/blog/search')
def blog_search():
    q = request.args.get('q')

    blogs = Blog_post.query.filter(Blog_post.heading.like(f'%{q}%')).paginate(per_page = 10,page = 1)

    latest_blogs = Blog_post.query.order_by(Blog_post.id.desc()).paginate(per_page=4,page =1)
    if blog in latest_blogs.items:
        latest_blogs.items.remove(blog)

    return render_template('blog.html',blogs = blogs.items,latest_blogs = latest_blogs,categories = Blog_categories.query.all())

