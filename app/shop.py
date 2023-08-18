from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from .models import *
from flask_login import current_user

shop = Blueprint('shop',__name__)

@shop.route('/shop',methods = ['POST','GET'])
def shops():
    page = request.args.get('page',1,type=int)
    items = Shop_item.query.paginate(per_page=10,page=page)
    return render_template('shop.html',
                           items = items,
                           categories = Shop_category.query.all()
                           )

@shop.route('/shopDetails/<string:name>',methods = ['POST','GET'])
def shopDetails(name):
    item = Shop_item.query.filter_by(name=name).first()
    similar_items = Shop_item.query.filter_by(category = item.category).paginate(per_page=4,page =1)
    return render_template('shopDetails.html', item=item, similar_items=similar_items.items)

@shop.route('/shop/<string:category>')
def filter_by_category(category):
    category = Shop_category.query.filter_by(category_name=category).first()
    items = Shop_item.query.filter_by(category = category.id).paginate(per_page=10,page=1)
    return render_template('shop.html',
                           items=items,
                           categories=Shop_category.query.all(),
                           )

@shop.route('/category/<string:language>')
def filter_by_language(language):
    items = Shop_item.query.filter_by(language=language).paginate(per_page=10,page=1)
    return render_template('shop.html',
                           items = items,
                           categories = Shop_category.query.all()
                           )
@shop.route('/<string:item_name>/review',methods = ['POST'])
def shop_item_review(item_name):
    name = request.form['name']
    email = request.form['email']
    review = request.form['review']

    if current_user.is_authenticated:
        image = 'default.jpg'
    else:
        image = 'default.jpg'

    item = Shop_item.query.filter_by(name = item_name).first()

    new_review = Shop_item_review(name=name,email=email,comment=review,image=image,parent_item=item.id)
    db.session.add(new_review)
    db.session.commit()
    flash('Your review has been added succesfully',category = 'success')
    return redirect(url_for('shop.shopDetails',name = item_name))
