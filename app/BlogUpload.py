from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from . import db
from .models import *
from werkzeug.utils import secure_filename
import os

BlogUpload = Blueprint('BlogUpload',__name__)

@BlogUpload.route('/blogUpload',methods = ['POST','GET'])
def blogUpload():
    if request.method == 'POST':
        heading = request.form['heading']
        highlight = request.form['highlight']
        caption = request.form['caption']
        category = request.form['category']
        author = request.form['author']
        image = request.files['image']

        new_blog = Blog_post(Image = secure_filename(image.filename),category = category,heading = heading,highlight=highlight,caption=caption,blog_creator = author)

        
        try:
            db.session.add(new_blog)
            db.session.commit()
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
            
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('blogUpload.html')
        
        flash('item successfully added to db',category='success')
        return redirect(url_for('BlogUpload.new_blog_heading',id = new_blog.id))

    return render_template('blogUpload.html',categories = Blog_categories.query.all(),authors = Blog_creators.query.all()) 

@BlogUpload.route('/delete-blog/<int:id>')
def delete_blog(id):
    blog = Blog_post.query.filter_by(id = id).first()
    db.session.delete(blog)
    db.session.commit()
    flash('Blog deleted successfully!',category='success')
    return redirect(url_for('dashboard.dashboard_blogs'))


@BlogUpload.route('/new-blog-heading/<int:id>',methods = ['POST','GET'])
def new_blog_heading(id):
    blog = Blog_post.query.filter_by(id = id).first()
    if request.method == 'POST':
        heading = request.form['heading']

        new_heading = Blog_heading(heading = heading,parent_blog = id)
        db.session.add(new_heading)
        db.session.commit()
        flash(f'New heading for blog <span style="color:blue;">{blog.heading}</span> has been added successfully!,You can click proceed to continue creating the blog or add another heading.',category = 'success')
        return redirect(url_for('BlogUpload.new_blog_heading',id = id))
    return render_template('new-blog-heading.html',
                           blog = blog
                           )

@BlogUpload.route('/new-blog-paragraph/<int:id>',methods = ['POST','GET'])
def new_blog_paragraph(id):
    blog = Blog_post.query.filter_by(id = id).first()
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        heading = request.form['heading']

        new_paragraph = Blog_paragraph(content = paragraph,parent_blog_heading = heading,parent_blog=id )
        db.session.add(new_paragraph)
        db.session.commit()
        flash('New paragraph added successfully!,you can click view blog to view the complete blog or add another another paragraph',category = 'success')
        return redirect(url_for('BlogUpload.new_blog_paragraph',id = id))
    return render_template('new-blog-paragraph.html',blog = blog)
      
    



@BlogUpload.route('/blogs/new-blog-creator',methods = ['POST','GET'])
def blogCreatorUpload():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
       

        new_BlogCreator = Blog_creators(name=name,
            Image = secure_filename(image.filename))
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)) 
        try:
            db.session.add(new_BlogCreator)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('blogCreatorUpload.html')
        
        blogCreator = Blog_creators.query.filter_by(id = new_BlogCreator.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('dashboard.dashboard_blog_creators'))
        #return render_template('blogUpload.html')  

    return render_template('new-blog-author.html') 

@BlogUpload.route('/delete-blog-author/<string:name>')
def delete_blog_author(name):
    author =  Blog_creators.query.filter_by(name = name).first()
    db.session.delete(author)
    db.session.commit()
    flash('Author successfully deleted',category = 'success')
    return redirect(url_for('dashboard.dashboard_blog_creators'))

# @BlogUpload.route('/blogViewUpload',methods = ['POST','GET'])
# def blogCreatorUpload():
#     if request.method == 'POST':
#         post_id = 1

#         new_viewer = Blog_view(
#             post_id = post_id
#         )
#         db.session.add(new_viewer)
#         db.session.commit()

#         blogViewer = Blog_view.query.filter_by(id = new_viewer.id).first()
#         return redirect(url_for('BlogUpload.blogCommentUpload',id = Blog_view.id))
    
#     return render_template('blogComment.html')
    
     

@BlogUpload.route('/blogCommentUpload',methods = ['POST','GET'])
def blogCommentUpload():
    if request.method == 'POST':
        post_id = 1
        comment = request.form['comment']
        user_id = 1
       
       

        new_BlogComment = Blog_comment(
            comment=comment,
           )
        try:
            db.session.add(new_BlogComment)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('blogComment.html')
        
        blogComment = Blog_comment.query.filter_by(id = new_BlogComment.id).first()
        flash('item successfully added to db',category='success')
        return redirect(url_for('BlogUpload.blogUpload',id = Blog_post.id))
        #return render_template('blogUpload.html')  

    return render_template('blogComment.html') 


@BlogUpload.route('/blogs/new-category',methods = ['POST','GET'])
def new_blog_category():
    if request.method == 'POST':
        name = request.form['name']

        new_category = Blog_categories(category_name = name)
        db.session.add(new_category)
        db.session.commit()
        flash('New blog category successfully added',category = 'success')
        return redirect(url_for('dashboard.dashboard_blog_categories'))
    return render_template('new-blog-category.html')

@BlogUpload.route('/delete-blog-categories/<string:name>')
def delete_blog_category(name):
    category = Blog_categories.query.filter_by(category_name = name).first()
    db.session.delete(category)
    db.session.commit()
    flash('Category successfully deleted!',category='success')
    return redirect(url_for('dashboard.dashboard_blog_categories'))

