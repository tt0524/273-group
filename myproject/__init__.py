import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


# Create a login manager object
login_manager = LoginManager()

app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration for Email Service
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'GMAIL USER NAME',
    MAIL_PASSWORD = 'GMAIL APP PASSWORD',
    MAIL_DEFAULT_SENDER = 'smart_coffee_maker'
))

db = SQLAlchemy(app)
Migrate(app,db)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"

## !! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
## Grab the blueprints from the other views.py files for each "app"
from myproject.devices.views import devices_blueprint
from myproject.menus.views import menus_blueprint
from myproject.brew.views import brew_blueprint
from myproject.login.views import login_blueprint
from myproject.products.views import products_blueprint


app.register_blueprint(devices_blueprint,url_prefix="/devices")
app.register_blueprint(menus_blueprint,url_prefix="/menus")
app.register_blueprint(brew_blueprint,url_prefix='/brew')
app.register_blueprint(login_blueprint,url_prefix='/login')
app.register_blueprint(products_blueprint,url_prefix='/products')
