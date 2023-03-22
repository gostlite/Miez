from miez_app import user_db, user_bk, user_not
from miez_app.forms import BookingForm
from miez_app.model import Booking
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId


post = Blueprint("post", __name__)

@post.get('/appointments')
@login_required
def appointment():
    # "accepted":True
    user = current_user.user_json
    mylist = list(user_bk.find({"user_id":str(user['_id'])}))
    print(user['_id'])
    print(type(user['_id']))
    print(len(mylist))
  
    return render_template('pages/appointment.html', bookings=mylist)


@post.get('/notifications')
@login_required
def notification():
    # "accepted":True
    user = current_user.user_json
    try:
        mylist = user_not.find({"user_id":str(user["_id"])})
    except BaseException:
        pass
    return render_template('pages/notifications.html', aList=mylist)

@post.route('/booking',methods=['GET', 'POST'])
@login_required
def booking():
    user = current_user.user_json
    form = BookingForm()
    # checking the free user
    print(user['membership'])
    print(user['trials'])
    if user['membership'] != "Free" :
        if form.validate_on_submit():    
            bookingsValid(form, user)
            return redirect(url_for('users.dashboard'))
        return render_template('pages/bookingForm.html', form = form)
    elif user['membership']  == 'Free' and user['trials'] > 0:
        if form.validate_on_submit():    
            bookingsValid(form, user)
            trials = user['trials']-1
            user['trials'] = trials
            user_db.find_one_and_update({"_id":ObjectId(user['_id'])}, {'$set':{"trials":trials}})
            return redirect(url_for('users.dashboard'))
        return render_template('pages/bookingForm.html', form = form)
    flash("Sorry your free trials is exausted, kindly select a plan to enjoy our services", 'danger')
    return redirect(url_for('users.payment'))


def bookingsValid(form, user):
    
    new_booking = Booking(time= str(form.time.data),
                         user_id= str(user['_id']),
                        date=str(form.date.data),
                        services=form.services.data,
                        address=form.address.data,details=form.details.data)
    user_bk.insert_one(new_booking.__dict__)
    flash(f"A new booking has been made for {form.date.data} by {form.time.data}, kindly keep checking your appointment page to see when it is approved")
    #link the bookings to the user
    #increase bookings
    user["booking"] = int(user["booking"]) + 1
    user_db.find_one_and_update({"_id":user["_id"]}, {"$set":{"booking":user["booking"]}})
    return