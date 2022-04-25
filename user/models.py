from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid
from mongoengine import connect, Document, StringField, ListField, ReferenceField, DictField
import json
import os

connect(db='test', host=os.getenv('DB_HOST'), port=27017)

class CardsUser(Document):
    _id = StringField(required = True)
    userName = StringField(required = True, max_length=64)
    email = StringField(required = True, max_length=64)
    password = StringField(reqired=True)

class CardsList(Document):
    _id = StringField(required = True)
    title = StringField(required = True, max_length=64)
    description = StringField(max_length=128)
    cards = ListField(DictField())
    owner_id = StringField(required = True)

class User:
    def start_session(self,user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        #Create to user object
        user = CardsUser(
            _id = uuid.uuid4().hex,
            userName = request.form.get('name'),
            email = request.form.get('email'),
            password = request.form.get('password')
        )

        # Encrypt password
        user.password = pbkdf2_sha256.encrypt(user['password'])

        # ADD MORE VALIDATION HERE LATER.

        # Save user to db and start session. 
        # Note: passing python dict of user
        if user.save():
            return self.start_session(json.loads(user.to_json()))

        return jsonify({'error': 'Signup failed'}), 400
    
    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        # Check if email match exists
        if CardsUser.objects(email=request.form.get('email')).count() != 0:
            user = json.loads(CardsUser.objects.get(email =request.form.get('email')).to_json())

            # Check if password match
            if pbkdf2_sha256.verify(request.form.get('password'), user['password']): 
                return self.start_session(user)

        # return error
        return jsonify({'error': 'Invalid login crdentials'}), 401

    # Add Cards list.
    def addCards(self):
        
        # Get person to save owner reference into into cardsList created.
        person = CardsUser.objects.get(email = session['user']['email'])
        
        cards = CardsList(
            _id = uuid.uuid4().hex,
            title = request.form.get('title'),
            description = request.form.get('description'),
            cards = [],
            owner_id = person._id  
        )
        cards.save()

        return jsonify({"success": "Sucess"}), 200

# Get a users Cards.
def GetUsersCardsLists(userEmail):
    user = CardsUser.objects.get(email = userEmail)
    usersCards = json.loads(CardsList.objects(owner_id = user._id).to_json())
    return usersCards
