
#import from current package
from . import db

#module that helps log users in 
from flask_login import UserMixin


from sqlalchemy.sql import func


class Note(db.Model): 

    id = db.Column (db.Integer, primary_key = True)
    note = db.Column(db.String(500))
    note_date = db.Column(db.DateTime(timezone=True), default=func.now())

    #associate note with a user - foreign key - set up a relationships
    #must pass valid id of existing user 
    # 1 to many - 1 user with many notes -  1 object with many children
    # foreign key of child object refers to parent object
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




#inherit from db object and also inherit from UserMixin object
#this is inheritance
class User(db.Model, UserMixin): 

    id = db.Column (db.Integer, primary_key = True)

    #no user can have same email as another user
    email = db.Column(db.String(80),unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    first_name = db.Column(db.String(80),nullable=False)

    #allow user to access all their notes
    # will be a list of different notes
    # should be capital
    notes = db.relationship('Note')
    

    


