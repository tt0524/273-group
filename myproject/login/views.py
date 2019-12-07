from flask import Blueprint,render_template,redirect,url_for,flash,abort,request
from myproject import db
from flask_login import login_user,login_required,logout_user
from myproject.login.forms import LoginForm, RegistrationForm
from myproject.models import User
from werkzeug.security import generate_password_hash, check_password_hash


login_blueprint = Blueprint('login',
                              __name__,
                              template_folder='templates/login')


@login_blueprint.route('/make', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('devices.list')

            return redirect(next)
    return render_template('login_login.html', form=form)

@login_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('login_welcome_user.html')


@login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    address=form.address.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login.login'))
    return render_template('login_register.html', form=form)


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))
