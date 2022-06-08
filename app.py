from typing_extensions import Required
from flask import Flask, render_template, redirect, session
from functools import wraps
import os
import json

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Decorators. (function will be passed in function (dashboard_render), decide if go though or not)
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs) #return orginial function trying to access
        else:
            return redirect('/') #redirect to home page
    return wrap

#Routes
from user import routes
from user.models import GetUsersCardsLists, GetSingleCardsList, GetPublicCards

@app.route('/', methods=['GET'])
def home():

    #Get recent 6 public flash cards.
    publicCards = GetPublicCards()
    publicCards = publicCards[0:6]

    return render_template('home.html', cards = publicCards)


@app.route('/dashboard/', methods=['GET'])
@login_required
def dashboard():
    #Get users cards list.
    userCards = GetUsersCardsLists(session['user']['userName'])
    
    return render_template('dashboard.html', cardsLists = userCards)

@app.route('/editCardsList/<string:title>', methods=['GET'])
@login_required
def editCardsList(title:str):
    # Get a single  cardsList.
    cardsList = GetSingleCardsList(session['user']['userName'], title)

    return render_template('editCardsList.html', cards = cardsList)

@app.route('/viewCards/<string:name>/<string:title>', methods=['GET'])
def ViewCards(name:str,title:str):
    # Get a single  cardsList.
    cardsList = GetSingleCardsList(name, title)

    # Check if cardsList if public.
    if cardsList['public'] == False:
        # If cardsList if private then return home if not logged in or if cardsList not owned by current user.
        if not session.get('logged_in') or session['user']['userName'] != cardsList['owner_name']:
            return redirect('/')

    return render_template('viewCards.html', cards = cardsList)