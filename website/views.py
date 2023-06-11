from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user
from .forms import UpdateProfile,UpdateContact
from .models import Event, Comment, Booking, User
from flask_wtf import FlaskForm
from .models import Event
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    events = Event.query.filter((Event.status!='["Unpublished"]')).all()
    pop = Event.query.filter((Event.genre=='["Pop"]'),(Event.status!='["Unpublished"]')).all()
    rnb = Event.query.filter((Event.genre=='["RnB"]'),(Event.status!='["Unpublished"]')).all()
    hip = Event.query.filter((Event.genre=='["Hip-Hop"]'),(Event.status!='["Unpublished"]')).all()
    rock = Event.query.filter((Event.genre=='["Rock"]'),(Event.status!='["Unpublished"]')).all()
    return render_template('index.html', user=current_user, events=events, pop=pop,rnb=rnb,hip=hip,rock=rock)

@views.route('/pop', methods=['GET', 'POST'])
def pop():

    pop = Event.query.filter((Event.genre=='["Pop"]')).all()

    return render_template('pop.html', pop=pop)

@views.route('/pop', methods=['GET', 'POST'])
def rnb():

    rnb = Event.query.filter((Event.genre=='["RnB"]')).all()

    return render_template('pop.html', rnb=rnb)


@views.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        evnt = "%" + request.args['search'] + '%'
        # Will find search in description or artist name
        events = Event.query.filter((Event.description.like(evnt)) | (Event.artist.like(evnt))).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))

@views.route('/profile', methods=['GET', 'POST'])
def profile():
    user = User.query.filter_by(id=current_user.id).first()

    #form
    pForm = UpdateProfile()
    contactForm = UpdateContact()
      #if pForm.nickname.data != None and len(pForm.nickname.data) > 0:
        #user.nickname = pForm.nickname.data
      #if pForm.interest.data != None and len(pForm.interest.data) > 0:
        #user.interest = pForm.interest.data
    #update profile
    if contactForm.submitContact.data and contactForm.validate():
      if contactForm.email.data != None and len(contactForm.email.data) > 0:
        user.email = contactForm.email.data
      if contactForm.mobile.data != None and len(contactForm.mobile.data) > 0:
        user.phone = contactForm.mobile.data
      if contactForm.company.data != None and len(contactForm.company.data) > 0:
        user.company = contactForm.company.data
      if contactForm.address.data != None and len(contactForm.address.data) > 0:
        user.address = contactForm.address.data
      db.session.commit()
      return redirect(url_for('views.profile'))
    else:
      print(contactForm.errors)
    
    if pForm.submitProfile.data and pForm.validate():
      if pForm.nickname.data != None and len(pForm.nickname.data) > 0:
        user.nickname = pForm.nickname.data
      if pForm.interest.data != None and len(pForm.interest.data) > 0:
        user.interest = pForm.interest.data
      try:
        imgUrl = check_upload_file(pForm)
        if len(imgUrl) > 0:
            user.img = imgUrl
      except:
        print("No image upload")
      db.session.commit()
      return redirect(url_for('views.profile'))
    else:
      print(pForm.errors)



    return render_template('account.html', user=current_user, pForm=pForm, contactForm=contactForm)

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