from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#define database object
db = SQLAlchemy()
DB_NAME = 'database.db'


#I think this is a factory function
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'James'

    #tells where database is stored inside same directory as __init__.py
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    #initialize database
    db.init_app(app)


    #need to tell flask where routes are
    #need to import blueprints 
    from .views import views 
    from .auth import auth 

    #register bluepirngs with flask application
    app.register_blueprint(views,url_prefix='/')
    #don't want anything for prefix
    app.register_blueprint(auth,url_prefix='/')

    #import in order to load before createing database
    from .models import User, Note

    create_database(app)

    #instantiate LoginManager instance
    login_manager = LoginManager()
    #knows where to redirect if user not logged in
    login_manager.login_view = 'auth.login'
    #also knows which app we will  use
    login_manager.init_app(app)

    #tells flask how to load user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#checks if database already exists
#if it doesn't, it will create it

def create_database(app):
    #use path module to determine if database exsits
    if not path.exists('website/' + DB_NAME):
        #same as what I did in the terminal for flask intro
        db.create_all(app=app)
        print('Created Database!')



