# Routes related to user.
from flask import Flask
from app import app
from user.models import User

@app.route("/user/signup", methods=["POST"])
def signup():
    return User().signup()

@app.route("/user/signout")
def signout():
    return User().signout()

@app.route("/user/login", methods=["POST"])
def login():
    return User().login()

@app.route("/user/addCards", methods=["POST"])
def addCards():
    return User().addCards()

@app.route("/user/deleteCards/<string:title>")
def deleteCards(title:str):
    return User().RemoveCardsList(title)

@app.route("/user/addCard", methods=["POST"])
def addCard():
    return User().addCard()

