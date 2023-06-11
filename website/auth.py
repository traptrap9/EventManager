from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
)
from sqlalchemy import true 
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Event
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, login_required, logout_user
from . import db
from .forms import LoginForm, RegisterForm
import re
import validators

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #create a blueprint
    logForm = LoginForm()
    if logForm.validate_on_submit():
        email = logForm.email.data
        password = logForm.password.data
        isEmailValid=validators.email(email)
        result=isinstance(isEmailValid, validators.ValidationFailure)
        user = User.query.filter_by(email=email).first()
    
        if user:
            if check_password_hash(user.password, password):
                flash("Login Successful", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash("Incorrect Password. Try again", category='error')
        elif result==True:
            flash("This E-mail is not valid. Check your E-mail",category='error')
        elif not user:
            flash("This user does not exist.", category='error')


    return render_template('login.html', logForm=logForm)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    regForm = RegisterForm()
    if regForm.validate_on_submit():
        fullName = regForm.fullName.data    
        email = regForm.email.data   
        mobile = regForm.mobile.data   
        password = regForm.password.data
        address = regForm.address.data   
        confirm = regForm.confirm.data
        isEmailValid=validators.email(email)
        result=isinstance(isEmailValid, validators.ValidationFailure)
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This user exist.", category='error')
        elif result:
            flash("Please check the E-mail. It is not E-mail",category='error')
        else:
            if password == confirm:
                newUser = User(fullName=fullName, email=email, password=generate_password_hash(password, method='sha256'), phone=mobile, address=address)
                db.session.add(newUser)
                db.session.commit()
                login_user(newUser, remember=True)
                flash("Logged in successfully!", category='success')
                return redirect(url_for('views.index'))
            else:
                flash("Passwords do not match. Please try again.", category='error')

    return render_template('register.html', regForm=regForm)



# this is the hint for a login function
# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         u1 = User.query.filter_by(name=user_name).first()
#         if u1 is None:
#             error='Incorrect user name'
#         elif not check_password_hash(u1.password_hash, password): # takes the hash and password
#             error='Incorrect password'
#         if error is None:
#             login_user(u1)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
