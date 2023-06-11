#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db=SQLAlchemy()
app=Flask(__name__)
DB_NAME = 'sitedata.sqlite'

#create a function that creates a web application
# a web server will run this web application
def create_app():
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    #from .models import User  # importing here to avoid circular references
    #@login_manager.user_loader
    #def load_user(user_id):
    #    return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.views, url_prefix='/')

    from . import auth
    app.register_blueprint(auth.auth, url_prefix='/')

    from . import events
    app.register_blueprint(events.bp)

    from .models import User, Event, Comment

    create_database(app)
    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

@app.errorhandler(404) 
def not_found(e):
  return render_template("404.html")

@app.errorhandler(500) 
def not_found(e):
    return render_template("500.html")

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
