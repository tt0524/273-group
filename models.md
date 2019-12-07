<!-- models -->
models:
---- server:
    devices:
      ---- id
      ---- model_no
      ---- model_name
      ---- serial_no
      ---- nick_name (by default: user_name's model_name)
      ---- owner_id
      ---- registration_time
      ---- is_working (boolean)

    users:
      ---- id
      ---- user_name
      ---- Email
      ---- address
      ---- password

    device_user_registration_event:
      ---- id
      ---- event_time
      ---- action: (register, unregister)
      ---- user_id

    menu:
      ---- id
      ---- menu_name
      ---- brew_time (mins/float)

    brews:
      ---- id
      ---- brew_start_time
      ---- brew_end_time
      ---- status (completed, cancelled)
      ---- user_id
      ---- menu_id
      ---- device_id

    products:
      ---- id
      ---- product_name
      ---- capsule_quantity
      ---- price

    orders:
      ---- id
      ---- order_time
      ---- user_id
      ---- product_id
      ---- quantity
      ---- order_price

<!-- Add data analysis function for client -->
<!-- Add notification sent from Server using socketio -->
