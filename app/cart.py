from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from .models import *
from flask_login import login_required,current_user

cart = Blueprint('cart',__name__)

@cart.route('/cart',methods = ['POST','GET'])
@login_required
def carts():
    tot = 0
    for item in current_user.cart_items:
        tot += item.quantity * item.cart_item_parent.price()
    return render_template('cart.html',sub_total = tot)

@cart.route('/add-to-cart/<string:item_name>',methods=['POST','GET'])
@login_required
def add_to_cart(item_name):
    if request.method == 'POST':
        quantity = request.form['quantity']

        item = Shop_item.query.filter_by(name=item_name).first()

        existing_product = Cart.query.filter_by(parent_product = item.id).filter(Cart.item_owner == current_user.id).first()

        if existing_product:
            existing_product.quantity = int(quantity) + int(existing_product.quantity)
            db.session.commit()
            flash('Item successfully added to cart',category='success')
            return redirect(url_for('cart.carts'))
        else:
            new_cart_item = Cart(parent_product=item.id,quantity=quantity,item_owner=current_user.id)
            db.session.add(new_cart_item)
            db.session.commit()
            flash('Item successfully added to cart',category='success')
            return redirect(url_for('cart.carts'))
    else:
        quantity = 1

        item = Shop_item.query.filter_by(name=item_name).first()

        existing_product = Cart.query.filter(Cart.parent_product == item.id ).filter(Cart.item_owner == current_user.id).first()

        if existing_product:
            existing_product.quantity = int(quantity) + int(existing_product.quantity)
            db.session.commit()
            flash('Item successfully added to cart',category='success')
            return redirect(url_for('cart.carts'))
        else:
            new_cart_item = Cart(parent_product=item.id,quantity=quantity,item_owner=current_user.id)
            db.session.add(new_cart_item)
            db.session.commit()
            flash('Item successfully added to cart',category='success')
            return redirect(url_for('cart.carts'))
@cart.route('/cart/delete-all')
@login_required
def delete_all():
    for item in current_user.cart_items:
        db.session.delete(item)
        db.session.commit()
    flash('All items have been successfully removed from cart',category='success')
    return redirect(url_for('cart.carts'))
    
    
            

        
        
@cart.route('/remove-from-cart/<int:id>')
@login_required
def remove_from_cart(id):
    item = Cart.query.filter_by(id = id).first()
    db.session.delete(item)
    db.session.commit()
    flash('tem removed from cart',category='success')
    return redirect(url_for('cart.carts'))


