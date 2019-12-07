from myproject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import time, datetime
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

##############
## Model - Device
##############
class Device(db.Model):

    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key = True)
    serial_numer = db.Column(db.String(12), unique=True, index=True)
    model_name = db.Column(db.String(128))
    nick_name = db.Column(db.String(256))
    owner_id = db.Column(db.Integer)
    registration_time = db.Column(db.DateTime)
    is_working = db.Column(db.Boolean)

    def __init__(self, serial_numer, model_name):
        self.serial_numer = serial_numer
        self.model_name = model_name
        self.is_working = False

    def __repr__(self):
        if self.owner_id:
            owner = User.query.get(self.owner_id)
            working = "is" if self.is_working else "is not"
            return "Device: serial number = {}, model_name = {}, owner = {}, {} working now".format(self.serial_numer, self.model_name, owner.username, working)
        else:
            working = "is" if self.is_working else "is not"
            return "Device: serial number = {}, model_name = {}, not registered by user yet, {} working now".format(self.serial_numer, self.model_name, working)

##############
## Model - User
##############
# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    address = db.Column(db.String(512), index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password, address):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.address = address

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)


##############
## Model - Device User Registration Event
##############
class RegEvent(db.Model):

    __tablename__ = 'regevents'

    id = db.Column(db.Integer,primary_key= True)
    event_time = db.Column(db.DateTime)
    action = db.Column(db.String(36))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))

    def __init__(self,event_time, action, user_id, device_id):
        self.event_time = event_time
        self.action = action
        self.user_id = user_id
        self.device_id = device_id

    def __repr__(self):
        return "User id = {} {} device id ={} at {}".format(self.user_id, self.action, self.device_id, self.event_time)

##############
## Model - Coffee Menus
##############
class Menu(db.Model):

    __tablename__ = 'menus'

    id = db.Column(db.Integer,primary_key= True)
    menu_name = db.Column(db.Text)
    brew_time = db.Column(db.Time)

    def __init__(self,menu_name, brew_time):
        self.menu_name = menu_name
        self.brew_time = brew_time

    def __repr__(self):
        return "Menu: {}, time to brew: {} min, {} sec".format(self.menu_name, self.brew_time.min, self.brew_time.sec )

##############
## Model - Coffee Brew Event
##############
class BrewEvent(db.Model):

    __tablename__ = 'brewevents'

    id = db.Column(db.Integer,primary_key= True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"))
    status = db.Column(db.String(64)) # status: cancelled, finished


    def __init__(self,start_time, user_id, device_id, menu_id):
        self.start_time = start_time
        self.user_id = user_id
        self.device_id = device_id
        self.menu_id = menu_id

    def __repr__(self):
        menu = Menu.query.get(self.menu_id)
        user = User.query.get(self.user_id)
        device = Device.query.get(self.device_id)
        return "User {} brewed {} using device {} at {}, {} at {}".format(user.username, menu.menu_name, device.model_name, self.start_time, self.status, self.end_time)
##############
## Model - Products
##############
class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(128))
    capsule_quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __init__(self, product_name, capsule_quantity, price):
        self.product_name = product_name
        self.capsule_quantity = capsule_quantity
        self.price = price

    def __repr__(self):
        return "{}: {} capsules/${}".format(self.product_name,self.capsule_quantity, self.price)

##############
## Model - Orders
##############
class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer)
    order_price = db.Column(db.Float)

    def __init__(self, order_time, user_id, product_id, quantity, order_price):
        self.order_time = order_time
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_price = order_price

    def __repr__(self):
        product = Product.query.get(self.product_id)
        user = User.query.get(self.user_id)
        return "User: {} ordered {} at {}, total price is ${}".format(user.username, product.product_name, self.order_time, self.order_price)
