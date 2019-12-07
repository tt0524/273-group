from flask import Blueprint,render_template,redirect,url_for,flash
from myproject import db
from flask_login import login_user,login_required,current_user
from myproject.devices.forms import RegisterDeviceForm,UnregisterDeviceForm
from myproject.models import Device, User, RegEvent
from datetime import datetime

devices_blueprint = Blueprint('devices',
                              __name__,
                              template_folder='templates/devices')

@login_required
@devices_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterDeviceForm()

    if form.validate_on_submit():
        serial_numer = form.serial_numer.data
        user_id = current_user.id
        device = Device.query.filter_by(serial_numer=serial_numer).first()
        action = "register"
        event_time = datetime.now()
        # Register a device
        new_regevent = RegEvent(event_time, action, user_id, device.id)
        db.session.add(new_regevent)

        # update the owner information in device table
        device.owner_id = user_id
        device.registration_time = event_time
        device.nick_name = current_user.username + "'s " + device.model_name

        db.session.commit()
        flash("Device Registered!!")
        return redirect(url_for('devices.list'))


    return render_template('register.html',form=form)

#@login_required
@devices_blueprint.route('/list')
def list():
    # Grab a list of clients from database.
    devices = Device.query.filter_by(owner_id=current_user.id).all()
    #devices = Device.query.all()
    ids = [device.id for device in devices]
    return render_template('list.html', devices=devices, ids=ids)

@login_required
@devices_blueprint.route('/unregister', methods=['GET', 'POST'])
def unregister():
    form = UnregisterDeviceForm()

    if form.validate_on_submit():
        serial_numer = form.serial_numer.data
        user_id = current_user.id
        device = Device.query.filter_by(serial_numer=serial_numer).first()
        action = "unregister"
        event_time = datetime.now()
        # Register a device
        new_regevent = RegEvent(event_time, action, user_id, device.id)
        db.session.add(new_regevent)

        # update the owner information in device table
        device.owner_id = None
        device.registration_time = None
        device.nick_name = None
        device.is_working = False

        db.session.commit()
        flash("Device Registered!!")
        return redirect(url_for('devices.list'))

    return render_template('unregister.html',form=form)

# @devices_blueprint.route('/discover/<id>')
# def discover(id):
#     device = Device.query.get(id)
#     if device.is_making_coffee:
#         coffee = Menu.query.get(device.coffee_in_production)
#         attribute = "Device: id = {}, name = {}, owner = {}, is making coffee:{}".format(device.id, device.name, device.owner, coffee.coffee_name)
#     else:
#         attribute = "Device: id = {}, name = {}, owner = {}, is currently idle".format(device.id, device.name, device.owner)
#     return render_template('discover.html', attribute=attribute)
