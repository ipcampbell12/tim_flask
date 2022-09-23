from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
#allows it to secure the password, never store in plain text, hash password 
#can't find original password
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

#works with user mixin
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)

#define routes for login/logout/signup
@auth.route('/login', methods = ['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #check if matches, return first(only) result
        user= User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!",category="sucess")

                #remembers that user is logged in, stored in flask session
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again", category = 'error')
        else:
            flash('Email does not exist',category='error')

    #return render_template('login.html',text="Your Mom",user="Ian")
    return render_template('login.html',user=current_user)

@auth.route('/logout')
#can't access this route unless you are logged in
@login_required
def logout():
    logout_user

    #returns to sign in page
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method ==  'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #check to make sure user doesn't already exist
        user= User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email) < 4: 
            flash('Email must be greater than 3 characters', category = 'error')
        elif len(first_name) < 2:
            flash ('First name must be greater than 1 character',category = 'error')
        elif password1 != password2: 
            flash ('Your passwords don\'t match',category = 'error')
        elif len(password1) <7:
            flash("Your password must be at least 7 charactrs",category = 'error')
        else:
            new_user = User(email=email,first_name =first_name, password= generate_password_hash(password1,method='sha256'))

            #add new user to db
            db.session.add(new_user)

            #update database
            db.session.commit()
            login_user(new_user, remember=True)
            
            flash("Account created!", category='success')
            #add ueser to database

            #redirect to home page
            #view is name of viewpoint, home is name of the function
            #find the url that matches
            return redirect(url_for('views.home'))
            

    #checks if user is logged in and sends to template
    return render_template('signup.html', user = current_user)

