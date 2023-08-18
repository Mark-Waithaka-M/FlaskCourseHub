from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from flask_login import login_required,current_user
from .models import *

wishlist = Blueprint('wishlist',__name__)

@wishlist.route('/wishlist',methods = ['POST','GET'])
@login_required
def wishlists():
    return render_template('wishlist.html')

@wishlist.route('/add-to-wishlist/<string:name>')
@login_required
def add_to_wishlist(name):
    course = Course.query.filter_by(name = name).first()

    new_wishlist_item = Wishlist(name = course.name,parent_course = course.id,owner = current_user.id,image = course.Image)
    db.session.add(new_wishlist_item)
    db.session.commit()
    flash('item successfully added to wishlist',category = 'success')
    return redirect(url_for('wishlist.wishlists'))

@wishlist.route('/remove-from-wishlist/<string:name>')
@login_required
def remove_from_wishlist(name):
    item = Wishlist.query.filter_by(name = name).first()
    db.session.delete(item)
    db.session.commit()
    flash('item successfully removed from wishlist',category='success')
    return redirect(url_for('wishlist.wishlists'))

