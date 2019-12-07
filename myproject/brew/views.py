from flask import Blueprint,render_template,redirect,url_for
from myproject import db
from myproject.models import Menu, BrewEvent
# from myproject.brew.forms import BrewCoffeeForm
from wtforms import StringField, IntegerField, SubmitField,RadioField
from myproject.models import Menu, Device
from flask_login import login_user,login_required,current_user
from flask_wtf import FlaskForm
from datetime import datetime, time, timedelta
from collections import Counter
import time
# from myproject.brew.forms import BrewCoffeeForm


brew_blueprint = Blueprint('brew',
                              __name__,
                              template_folder='templates/brew')

@login_required
@brew_blueprint.route('/brew', methods=['GET', 'POST'])
def brew():

    menus = Menu.query.all()
    menu_choices = [(menu.id, menu.menu_name + ", time needed: " + str(menu.brew_time.minute) + " mins " + str(menu.brew_time.second) + " secs" ) for menu in menus]

    # available_devices = Device.query.filter_by(owner_id=current_user.id).all()
    # device_choices = [(device.id, device.nick_name) for device in available_devices]

    brews = BrewEvent.query.filter_by(user_id=current_user.id,end_time=None).all()
    for brew in brews:
        brew_time = Menu.query.get(brew.menu_id).brew_time
        print(brew_time)
        # brew_finish_time = brew.start_time
        # new_second = (brew.start_time.second + brew_time.second) % 60
        # if (brew.start_time.second + brew_time.second) // 60 > 1:
        #     new_minute = brew.start_time.minute + brew_time.minute + 1
        # else:
        #     new_minute = brew.start_time.minute + brew_time.minute
        # if new_minute // 60 > 0:
        #     new_hour = brew.start_time.hour + 1
        #     new_minute = new_minute % 60
        # else:
        #     new_hour = brew.start_time.hour + brew_time.hour
        # brew_finish_time.replace(hour=new_hour,minute=new_minute, second=new_second)
        brew_finish_time = (brew.start_time + timedelta(hours=0,minutes=brew_time.minute, seconds=brew_time.second))
        print("brew_finish_time:{}".format(brew_finish_time))
        print("now: {}".format(datetime.now()))
        if datetime.now() > brew_finish_time:
            brew.end_time = brew_finish_time
            brew.status = "finished"
            device = Device.query.get(brew.device_id)
            device.is_working = False
            db.session.commit()


    available_devices = Device.query.filter_by(owner_id=current_user.id,is_working=False).all()
    device_choices = [(device.id, device.nick_name) for device in available_devices]

    unavailable_devices = Device.query.filter_by(owner_id=current_user.id,is_working=True).all()
    working_devices = [device.nick_name for device in unavailable_devices]

    class BrewCoffeeForm(FlaskForm):

        brew_menu = RadioField("Select Menu", choices=[],coerce=int)
        brew_device = RadioField("Select Devices", choices=[],coerce=int)
        # working_device = RadioField("Working Devices", choices=select_device, render_kw={'readonly': True, 'disabled':True})
        submit = SubmitField('Brew Coffee!')

    form = BrewCoffeeForm()
    form.brew_menu.choices = menu_choices
    form.brew_device.choices = device_choices

    if form.validate_on_submit():
        menu_id = form.brew_menu.data
        device_id = form.brew_device.data
        user_id = current_user.id
        start_time = datetime.now()
        new_brew = BrewEvent(start_time, user_id, device_id, menu_id)
        device = Device.query.get(device_id)
        device.is_working = True
        db.session.add(new_brew)
        db.session.commit()
        # brew_coffee(new_brew)
        return redirect(url_for('brew.usage'))
    else:
        pass
        print(form.brew_menu.data)
        print(form.errors)
        # return redirect(url_for('brew.usage'))
    return render_template('brew.html',form=form, working_devices=working_devices)

# def brew_coffee(new_brew):
#     menu_id = new_brew.menu_id
#     menu = Menu.query.get(menu_id)
#     brew_time = menu.brew_time
#     sleep_time = brew_time.minute * 60 + brew_time.second
#     time.sleep(sleep_time)
#     new_brew.end_time = datetime.now()
#     new_brew.status = "finished"
#     db.session.commit()


@login_required
@brew_blueprint.route('/usage', methods=['GET', 'POST'])
def usage():
    # Grab a list of clients from database.
    brewevents = BrewEvent.query.filter_by(user_id=current_user.id).order_by(BrewEvent.start_time.desc()).all()
    coffees = [be.menu_id for be in brewevents]
    c_count = Counter(coffees)
    top1_menu_id = c_count.most_common(1)[0][0]
    top1 = Menu.query.get(top1_menu_id).menu_name
    recent = BrewEvent.query.filter_by(user_id=current_user.id).order_by(BrewEvent.start_time.desc()).first()
    rc = Menu.query.get(recent.menu_id).menu_name
    return render_template('usage.html', brewevents=brewevents, top1=top1,recent=rc)
