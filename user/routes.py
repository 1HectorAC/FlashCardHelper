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

@app.route("/user/deleteCard/<string:title>/<int:cardNumber>")
def deleteCard(title:str, cardNumber:int):
    return User().RemoveCard(title, cardNumber)

@app.route("/user/editCards", methods=["POST"])
def editCards():
    return User().EditCards()

@app.route("/user/editCard", methods=["POST"])
def editCard():
    return User().EditCard()

@app.route("/user/editName", methods=["POST"])
def editName():
    return User().EditName()

@app.route("/user/editEmail", methods=["POST"])
def editEmail():
    return User().EditEmail()

@app.route("/user/editPassword", methods=["POST"])
def editPassword():
    return User().EditPassword()
