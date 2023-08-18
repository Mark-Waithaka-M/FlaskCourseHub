from flask import Blueprint,render_template,redirect,request,url_for,flash,abort,current_app
from flask_login import current_user,login_required
from .models import *
import random
import string
import stripe

checkout = Blueprint('checkout',__name__)

@checkout.route('/checkout',methods = ['POST','GET'])
@login_required
def checkout_page():
    sub_total = 0
    for item in current_user.cart_items:
        sub_total += item.cart_item_parent.price() * item.quantity

    return render_template('checkout.html',sub_total = sub_total)

#-----------------pay with cash--------------------------
@checkout.route('/checkout/pay-with-cash')
@login_required
def pay_with_cash():
    addresses = Billing_details.query.filter_by(account_user = current_user.id).all()
    if len(addresses) == 0:
        flash('Please add billing address to place an order',category='danger')
        return redirect(url_for('checkout.checkout_page'))
    
    total = 0
    for item in current_user.cart_items:
        total += item.cart_item_parent.price() * item.quantity

    if total != 0:
        total += 5

    length = 4
    characters = string.digits
    identifier = ''.join(random.choice(characters) for i in range(length))

    new_order = Order(identifier=identifier,total = total,account_user=current_user.id,)

    db.session.add(new_order)
    db.session.commit()

    for item in current_user.cart_items:
        new_order_item = Order_item(shop_product = item.parent_product,quantity=item.quantity,parent_order = new_order.id)
        db.session.add(new_order_item)
        db.session.commit()

    for item in current_user.cart_items:
        db.session.delete(item)
        db.session.commit()
    
    
    return render_template('Payment-on-delivery-success.html')
#--------------------------------------stripe checkout----------------------
@checkout.route('/stripe-pay')
@login_required
def stripe_checkout():
    line_items = []
    for item in current_user.cart_items:
        line_item = {
        'price_data':{
                         'currency':'usd',
                         'unit_amount':item.cart_item_parent.price()  * 100,
                         'product_data':{
                                    'name':f'{item.cart_item_parent.name}',
                                    
                         }
        },
        'quantity':item.quantity,
        }
        line_items.append(line_item)

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    session = stripe.checkout.Session.create(
        payment_method_types =['card'],
        line_items = line_items,
        mode='payment',
        success_url = url_for('checkout.checkout_success',_external=True) + '?{CHECKOUT_SESSION_ID}',
        cancel_url = url_for('checkout.checkout_page',_external=True)

    )

    return {
        'checkout_session_id':session['id'],
        'checkout_public_key':current_app.config['STRIPE_PUBLIC_KEY']
    }
    
@checkout.route('/success')
def checkout_success():
    total = 0
    for item in current_user.cart_items:
        total += item.cart_item_parent.price() * item.quantity

    if total != 0:
        total += 5

    length = 4
    characters = string.digits
    identifier = ''.join(random.choice(characters) for i in range(length))

    new_order = Order(identifier=identifier,total = total,account_user=current_user.id,)

    db.session.add(new_order)
    db.session.commit()

    for item in current_user.cart_items:
        new_order_item = Order_item(shop_product = item.parent_product,quantity=item.quantity,parent_order = new_order.id)
        db.session.add(new_order_item)
        db.session.commit()

    for item in current_user.cart_items:
        db.session.delete(item)
        db.session.commit()

    return render_template('checkout-success.html')



#---------------Billing details------------------------------

#adding new billing details
@checkout.route('/add-new-billing-details',methods = ['POST','GET'])
@login_required
def add_billing_details():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            country = request.form['country']
            street_address = request.form['street_address']
            apartment = request.form['apartment']
            town = request.form['town']
            state = request.form['state']
            zip_code = request.form['zip-code']
            phone = request.form['phone']
            email = request.form['email'] 

            try:
                company_name = request.form['company_name']
            except:
                company_name = 'n/a'

            new_address = Billing_details(first_name = first_name,last_name=last_name,country=country,\
                                          street_address=street_address,apartment=apartment,town=town,state=state,zip_code=zip_code,\
                                            phone=phone,email=email,company_name=company_name,account_user=current_user.id)
            db.session.add(new_address)
            db.session.commit()
            flash('Billing Address has been added successfully',category='success')
            return redirect(url_for('checkout.checkout_page'))
        


        except Exception as e:
            print(e)
            flash('Every field with an asterisk(*) is required!',category ='danger') 
            return redirect(url_for('checkout.checkout_page')) 
    else:
        return redirect(url_for('checkout.checkout_page'))
        


        
