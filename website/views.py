#store standard pages for website 

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#define file is blueprint for application
views = Blueprint('views',__name__)

#slash is route for home page
#this function runs whenever we go to the main page of website
@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Your note is too short",category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Your note has been added to the database", category='success')




    # reference current_user and check if authenticated
    return render_template('home.html',user=current_user)

#@login_required means you can't get to home page unless you are logged in


@views.route('/delete-note',methods=['POST'])
def delete_note():

    #turn string into python dict object
    note = json.loads(request.data)
    noteId = note['note']
    note= Note.query.get(noteId)

    if note: 
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify()
