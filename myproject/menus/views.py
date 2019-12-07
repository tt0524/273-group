from flask import Blueprint,render_template,redirect,url_for
from myproject import db
from myproject.models import Menu
from myproject.menus.forms import AddForm

menus_blueprint = Blueprint('menus',
                              __name__,
                              template_folder='templates/menus')

@menus_blueprint.route('/list')
def list():
    # Grab a list of clients from database.
    menus = Menu.query.all()
    return render_template('list_menu.html', menus=menus)

@menus_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data

        # Register a new client
        new_menu = Menu(name)
        db.session.add(new_menu)
        db.session.commit()

        return redirect(url_for('menus.list'))

    print("New Coffee Added to Menu!!")
    return render_template('add.html',form=form)
