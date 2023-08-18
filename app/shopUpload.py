from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from . import db
from .models import *
from werkzeug.utils import secure_filename
import os
from flask_login import login_required

shopUpload = Blueprint('shopUpload',__name__)



@shopUpload.route('/shopItemUpload',methods = ['POST','GET'])  
def shopItemUpload():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        caption = request.form['caption']
        description = request.form['description']
        stock = request.form['stock']
        sku = request.form['sku']
        language = request.form['language']
        category = request.form['category']
        image = request.files['image']

        new_product = Shop_item(name=name,author = author,caption=caption,description=description,stock=stock,sku=sku,language=language,category=category,image = secure_filename(image.filename))
        
      
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
        try:
            db.session.add(new_product)
            db.session.commit()
        except:
            flash('Error in upload,try again later',category = 'danger')
            return render_template('shop-item.html',categories = Shop_category.query.all())
        
        flash('item successfully added to db',category='success')
        return redirect(url_for('shopUpload.shopItemUpload'))
    
    return render_template('shop-item.html',categories = Shop_category.query.all())

@shopUpload.route('/delete-shop-item/<string:name>')
@login_required
def delete_shop_item(name):
    item = Shop_item.query.filter_by(name = name).first()
    db.session.delete(item)
    db.session.commit()
    flash('Shop item deleted successfully!',category='success')
    return redirect(url_for('dashboard.dashboard_shop'))

@shopUpload.route('/upload/new-category',methods = ['POST','GET'])
def new_shop_category():
    if request.method == 'POST':
        category = request.form['category']

        new_category = Shop_category(category_name=category)
        db.session.add(new_category)
        db.session.commit()
        flash('new category has been added successfully!',category='success')
        return redirect(url_for('dashboard.dashboard_shop_categories'))
    return render_template('new-shop-category.html')

@shopUpload.route('/delete-shop-category/<int:id>')
def delete_shop_category(id):
    category = Shop_category.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    flash('item deleted successfully',category='success')
    return redirect(url_for('dashboard.dashboard_shop_categories'))


@shopUpload.route('/new-shop-tag/<int:id>',methods=['POST','GET'])
def add_new_tag(id):
    item = Shop_item.query.filter_by(id=id).first()
    if request.method == 'POST':
        tag_content = request.form['content']

        new_tag = Shop_item_tag(parent_item=id,tag_content=tag_content)
        db.session.add(new_tag)
        db.session.commit()
        flash('Item successfully added to db',category='success')
        return redirect(url_for('shopUpload.add_new_tag',id=id))
    return render_template('new-tag.html',item=item)

@shopUpload.route('/shop-item-price/<int:id>',methods = ['POST','GET'])
def item_price(id):
    item = Shop_item.query.filter_by(id=id).first()
    if request.method == 'POST':
        price = request.form['price']
        new_price = Shop_item_charter(parent_item=id,price=price)
        db.session.add(new_price)
        db.session.commit()
        flash('Item price added successfully',category='success')
        return redirect(url_for('dashboard.dashboard_shop'))
    return render_template('shop-item-price.html',item = item)







