from flask import Blueprint, render_template, redirect, flash, request, session, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
import json
from . import db, app
from datetime import datetime

from .forms import CreateEvent, CommentForm, BookEvent, UpdateEvent
from . import db
from .views import views
from .models import Event, Comment, Booking

import os

bp = Blueprint('event', __name__, url_prefix='/events')



@bp.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
  Event.query.filter_by(id=id).delete()
  Comment.query.filter(Comment.event_id==id).delete()
  Booking.query.filter(Booking.event_id==id).delete()
  db.session.commit()

  flash("Event Deleted Successfully", category="success")
  return redirect(url_for('views.index'))

@bp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = Event.query.filter_by(id=id).first()
    genreArr = parseGenre(event) # Converts json string back to list 

    # Forms
    cform = CommentForm()
    bForm = BookEvent()
    uForm = UpdateEvent()
    serializedStatus = json.dumps(uForm.status.data)

    # Booking Tickets
    if bForm.submitBuy.data and bForm.validate():
      ticketAmnt = bForm.buyTickets.data
      # if amount of buying tickets is available and greater than 0
      if ticketAmnt <= event.tickets and ticketAmnt > 0:
        totalPrice = ticketAmnt * event.ticketPrice

        # Create new booking & update event available tickets
        newBooking = Booking(ticketsBought=ticketAmnt, checkoutPrice=totalPrice, user_id=current_user.id, event_id=event.id, event_artist=event.artist, event_description=event.description, event_img=event.imgUrl)
        event.tickets = event.tickets - ticketAmnt

        if event.tickets == 0:
          event.status = "Sold Out"
        db.session.add(newBooking)
        db.session.commit()
        
        flash(f"Booking successful. You've been charged ${totalPrice}. Your booking id is {newBooking.id+1000000}. Check your profile if you want order number", category="success")
      else:
        flash("The amount of tickets you've tried to book exceeds the amount available or you've entered zero", category='error')
        return redirect(url_for('event.show', id=event.id))

    # Update Event
    if uForm.submitUpdate.data and uForm.validate():
      try:
        imgUrl = check_upload_file(uForm)
        if len(imgUrl) > 0:
          event.imgUrl = imgUrl
      except:
        print("No image upload")

      print(uForm.artistName.data)
      if len(uForm.artistName.data) > 0:
        event.artist = uForm.artistName.data
      if len(uForm.venue.data) > 0:
        event.venue = uForm.venue.data
      if len(uForm.description.data) > 0:
        event.description = uForm.description.data
      if uForm.dTime.data is not None:
        event.dTime = uForm.dTime.data
      if uForm.tickets.data is not None:
        event.tickets = uForm.tickets.data
        if event.tickets > 0:
          event.status = "Upcoming"
      if uForm.ticketPrice.data is not None:
        event.ticketPrice = uForm.ticketPrice.data
      if serializedStatus:
        event.status = serializedStatus
      if bool(uForm.genre.data):
        try:
          serializedGenre = json.dumps(uForm.genre.data)
          event.genre = serializedGenre
        except:
          print("No genre")
      db.session.commit()
      return redirect(url_for('event.show', id=event.id))
    else:
      print(uForm.errors)

    return render_template('events/eventDetails.html', event=event, uForm=uForm, bForm=bForm, form=cform, genreArr=genreArr)


def parseGenre(event):
  genreArr = json.loads(event.genre)
  return genreArr


def get_event():
    artist = 'Aubrey Drake Graham'
    description = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestias necessitatibus voluptates nemo, eos enim eligendi explicabo provident nostrum tenetur perferendis similique praesentium, ipsa consequatur corporis, iure repellat exercitationem quo autem.'
    img_link = 'https://static.dezeen.com/uploads/2018/11/drake-set-design-willo-perron-migos-tour_dezeen_sq.jpg'
    venue = 'Brisbane Showgrounds, 600 Gregory Terrace Bowen Hills QLD 4006'

    event = Event(artist, venue, description, '20/10/2022', 
     '8:30 pm - 12:30 am AEST', 28, img_link, 'RAP | HIP-HOP | RNB')

    comment = Comment("Mary Sue", "I've been to previous events but this one is going to be so good",'14 Aug 2022')
    event.set_comments(comment)
    comment = Comment("Bill", "free food!", '2019-11-12 11:00:00')
    event.set_comments(comment)
    comment = Comment("Sally", "free face masks!",'2019-11-12 11:00:00')
    event.set_comments(comment)
    return event


@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  eventForm = CreateEvent()
  if eventForm.validate_on_submit():
    imgUrl = check_upload_file(eventForm)
    serializedGenre = json.dumps(eventForm.genre.data)
    serializedStatus = json.dumps(eventForm.status.data)
    newEvent = Event(artist=eventForm.artistName.data, venue=eventForm.venue.data,
     description=eventForm.description.data, dTime=eventForm.dTime.data, 
     tickets=eventForm.tickets.data, ticketPrice=eventForm.ticketPrice.data, 
     imgUrl=imgUrl, genre=serializedGenre, status=serializedStatus, user_id=current_user.id)
    db.session.add(newEvent)
    db.session.commit()
    flash('Successfully created new event', category='success')
    return redirect(url_for('views.index'))
  else:
    print(eventForm.errors)
  return render_template('events/eventCreation.html', eventForm=eventForm)

@bp.route('/unpublished/', methods = ['GET', 'POST'])
@login_required
def unpublished():
  events = Event.query.filter_by(user_id=current_user.id, status='["Unpublished"]').all()
  uForm = UpdateEvent()

  return render_template('unpublished.html',events=events, uForm=uForm)

@bp.route('/<event>/comment', methods = ['GET', 'POST'])
@login_required
def comment(event):
  #here the form is created  form = CommentForm()
  flash("Successfully created comment", category="success")
  form = CommentForm()
  event_obj = Event.query.filter_by(id=event).first()  
  if form.validate_on_submit():	#this is true only in case of POST method
    comment = Comment(contents=form.contents.data,
                      user_id=current_user.id,
                      event=event_obj)
    db.session.add(comment) 
    db.session.commit() 
  return redirect(url_for('event.show', id=event))


def check_upload_file(form): # I've taken this from Week 9 Tutorial - Levi
  try:
    fp=form.image.data
    filename=fp.filename
    BASE_PATH=os.path.dirname(__file__)
    upload_path=os.path.join(BASE_PATH,'static\\images\\user',secure_filename(filename)) # /home/lia/Documents/repos/IAB207_Ass3/website/static/images/user SWAPPED AROUND CAUSE I USE LINUX ON ONE OF MY MACHINES
    db_upload_path='\\static\\images\\user\\' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path
  except:
    print("Error Checking Upload")
  