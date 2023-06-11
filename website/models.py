from email.policy import default
from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_login import current_user

class User(db.Model, UserMixin):
    #__tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(50), nullable=True)
    company = db.Column(db.String(30), nullable=True)
    nickname = db.Column(db.String(20), nullable=True)    
    interest = db.Column(db.String(30), nullable=True)
    img = db.Column(db.String(255))
    events = db.relationship('Event')
    comments = db.relationship('Comment')
    bookings = db.relationship('Booking')

    # relation to call user.comments and comment.created_by
    events = db.relationship('Event', backref='user')
    comments = db.relationship('Comment', backref='user')
    bookings = db.relationship('Booking', backref='user')



class Event(db.Model):
    #__tablename__ = 'events'
    def __init__(self, artist, venue, description, dTime, tickets, ticketPrice, imgUrl, genre, user_id,status):
        self.artist = artist
        self.venue = venue
        self.description = description
        self.dTime = dTime
        self.tickets = tickets
        self.ticketPrice = ticketPrice
        self.imgUrl = imgUrl
        self.genre = genre
        #self.comments = list()
        self.user_id = user_id
        self.status =status
    
    #def set_comments(self,comment):
    #    self.comments.append(comment)

    def __repr__(self): #string print method
        return "<Name: {}>".format(self.artist)

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(50))
    venue = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    dTime = db.Column(db.DateTime)
    # add a date posted1
    tickets = db.Column(db.Integer)
    ticketPrice = db.Column(db.Float(precision=2))
    imgUrl = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    dateCreated = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(25), default="Upcoming")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='event')

    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    #comments = db.relationship('Comment', backref='event')


class Comment(db.Model):
    __tablename__ = 'comments'
    
    def __repr__(self):
        return "<Comment: {}>".format(self.contents)
    
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(2500))
    date = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))



class Booking(db.Model):
    def __init__(self, ticketsBought, checkoutPrice, user_id, event_id,event_artist,event_description,event_img):
        self.ticketsBought = ticketsBought
        self.checkoutPrice = checkoutPrice
        self.user_id = user_id
        self.event_id = event_id
        self.event_artist = event_artist
        self.event_description = event_description
        self.event_img = event_img

    id = db.Column(db.Integer, primary_key=True)
    ticketsBought = db.Column(db.Integer) # Need to include a check for if tickets bought exceed available tickets
    checkoutPrice = db.Column(db.Integer) # Sum of tickets bought * price of event ticket
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event_artist = db.Column(db.Integer, db.ForeignKey('event.artist'))
    event_description = db.Column(db.Integer, db.ForeignKey('event.description'))
    event_img = db.Column(db.Integer, db.ForeignKey('event.imgUrl'))
    date = db.Column(db.DateTime, default=datetime.now())
