from wsgiref.validate import validator
from xmlrpc.client import DateTime
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, DateTimeLocalField, SelectMultipleField, FileField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo,Optional,Regexp
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime

ALLOWED_FILE = {'PNG','JPG','png','jpg', 'JPEG', 'jpeg'}

#creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email Address", validators=[InputRequired('Enter user password')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])

# this is the registration form
class RegisterForm(FlaskForm):
    fullName=StringField("Full Name", validators=[InputRequired()])
    mobile = StringField("Mobile Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired('Enter user password')])
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")


class CreateEvent(FlaskForm):
    artistName = StringField("Artists Name", validators = [InputRequired("Please list the artists name")])
    venue = StringField("Venue", validators = [InputRequired("Please enter a name for the venue")])
    description = TextAreaField("Description", validators = [InputRequired("Please enter a short description of the event")])
    dTime = DateTimeLocalField("Date and Time of Event", format="%Y-%m-%dT%H:%M")
    tickets = IntegerField("Number of Tickets Available")
    ticketPrice = DecimalField("Please enter the price per ticket", places=2)
    image = FileField('Preview Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    genre = SelectMultipleField(choices=['Hip-Hop', 'Pop', 'RnB', 'Rock'],validators=[InputRequired()])
    status = SelectMultipleField(choices=['Upcoming', 'Unpublished'],validators=[InputRequired()])
    submit = SubmitField("Create Event")


class UpdateEvent(FlaskForm):
    artistName = StringField("Artists Name")
    venue = StringField("Venue")
    description = TextAreaField("Description")
    dTime = DateTimeLocalField("Date and Time of Event", format="%Y-%m-%dT%H:%M", validators=[Optional(strip_whitespace=True)])
    tickets = IntegerField("Number of Tickets Available", validators=[Optional(strip_whitespace=True)])
    ticketPrice = DecimalField("Please enter the price per ticket", places=2, validators=[Optional(strip_whitespace=True)])
    image = FileField('Preview Image', validators=[FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG'), Optional(strip_whitespace=True)])
    genre = SelectMultipleField(choices=['Hip-Hop', 'Pop', 'RnB', 'Rock'], validators=[Optional(strip_whitespace=True)])
    status = SelectMultipleField(choices=['Upcoming', 'Unpublished'])
    submitUpdate = SubmitField("Save Changes")

class UpdateProfile(FlaskForm):
    nickname = StringField("Nickname")
    interest = StringField("Interst music")
    image = FileField('Preview Image', validators=[FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG'), Optional(strip_whitespace=True)])
    submitProfile = SubmitField("Save Changes")

class UpdateContact(FlaskForm):
    email = StringField("E-mail")
    mobile = StringField("Mobile")
    address = StringField("Address")
    company = StringField("Company")
    submitContact = SubmitField("Save Changes")
class BookEvent(FlaskForm):
    buyTickets = IntegerField("Please enter the amount of tickets you'd like to buy", validators=[InputRequired("Please enter the amount of tickets you'd like to purchase")])
    submitBuy = SubmitField("Book Tickets")


class CommentForm(FlaskForm):
  contents = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Submit')