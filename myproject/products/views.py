from flask import Blueprint,render_template,redirect,url_for
from myproject import db
from myproject.models import Product, Order
from myproject.products.forms import Buy
from datetime import datetime
from flask_login import login_user,login_required,current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,RadioField


products_blueprint = Blueprint('products',
                              __name__,
                              template_folder='templates/products')

@login_required
@products_blueprint.route('/buy',methods=['GET', 'POST'])
def buy():

    class Buy(FlaskForm):

        select_product = RadioField("Select Product", choices=[],coerce=int)
        submit = SubmitField('Purchase!')

    products = Product.query.all()
    choices = [(product.id, product) for product in products]

    form = Buy()
    form.select_product.choices = choices

    if form.validate_on_submit():
        order_time = datetime.now()
        user_id = current_user.id
        product_id = form.select_product.data
        quantity = 1
        product = Product.query.get(product_id)
        order_price = product.price
        new_order = Order(order_time, user_id, product_id, quantity, order_price)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('products.billing'))
    else:
        print(form.errors)
        pass
    return render_template('buy.html', form=form)


@login_required
@products_blueprint.route('/billing')
def billing():
    # Grab a list of clients from database.
    orders = Order.query.order_by(Order.order_time.desc()).all()
    return render_template('billing.html', orders=orders)

# @orders_blueprint.route('/make', methods=['GET', 'POST'])
# def make():
#
#     form = MakeOrderForm()
#
#     if form.validate_on_submit():
#         device_id = form.device_id.data
#         menu_id = form.menu_id.data
#         new_order = Order(device_id,menu_id)
#         device = Device.query.get(device_id)
#         device.is_making_coffee = True
#         device.coffee_in_production = menu_id
#         db.session.add(new_order)
#         db.session.commit()
#
#         return redirect(url_for('orders.list'))
#
#     return render_template('make.html',form=form)
