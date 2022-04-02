from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid
from mongoengine import connect, Document, StringField, ListField, DictField
import json
import os

connect(db="test", host=os.getenv('DB_HOST'), port=27017)

class CardsUser(Document):
    _id = StringField(required = True)
    userName = StringField(required = True, max_length=64)
    email = StringField(required = True, max_length=64)
    password = StringField(reqired=True)

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

        return jsonify({"error": "Signup failed"}), 400
    
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

        # retur error
        return jsonify({"error": "Invalid login crdentials"}), 401