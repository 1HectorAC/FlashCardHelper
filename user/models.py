from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid
from mongoengine import connect, Document, StringField, ListField, DictField, BooleanField, DateTimeField
from mongoengine.queryset.visitor import Q
from datetime import datetime
import json
import os

connect(db='test', host=os.getenv('DB_HOST'), port=27017)

class CardsUser(Document):
    _id = StringField(required = True)
    userName = StringField(required = True, max_length=64, unique=True)
    email = StringField(required = True, max_length=64)
    password = StringField(reqired=True)

class CardsList(Document):
    _id = StringField(required = True)
    title = StringField(required = True, max_length=64)
    description = StringField(max_length=128)
    public = BooleanField()
    cards = ListField(DictField())
    owner_name = StringField(required = True)
    timestamp = DateTimeField(default=datetime.utcnow)

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
        # Unique username check.
        nameExitsCheck = CardsUser.objects(userName = user.userName)
        if(nameExitsCheck):
            return jsonify({'error': 'Signup failed. UserName Already Exits'}), 400
        # Unique username check.
        emailExitsCheck = CardsUser.objects(email = user.email)
        if(emailExitsCheck):
            return jsonify({'error': 'Signup failed. Email Already Exits'}), 400

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
            public = True if request.form.get('public') == "true" else False,
            cards = [],
            owner_name = person.userName  
        )
        cards.save()

        return jsonify({"success": "Sucess"}), 200

    # Delete Cards list.
    def RemoveCardsList(self, cardTitle):
        # Get cards list of given title that is owned by the user
        cardsList = CardsList.objects(Q(title = cardTitle) & Q(owner_name = session['user']['userName']))
        
        # Delete object if exits.
        if(cardsList):
          cardsList.delete()

        return redirect('/dashboard/')

    # Add a card to cards list
    def addCard(self):
        questionList = request.form.getlist('questionPart')
        answerList = request.form.getlist('answerPart')
        cardsTitle = request.form.get('cardsTitle')
        
        # Setup data to add.
        data = []
        if "" not in questionList and "" not in answerList and len(questionList) == len(answerList):
            for x in range(0, len(questionList)):
                data.append({'question' : questionList[x], 'answer' : answerList[x]})

        # Added cards to cardslist
        CardsList.objects(Q(title = cardsTitle) & Q(owner_name = session['user']['userName'])).update_one(push_all__cards = data)
        
        return jsonify({"success": "Sucess"}), 200

    # Delete a card from the card list.
    def RemoveCard(self, cardTitle, cardNumber):
        # Get cards list of given title that is owned by the user.
        cardsList = CardsList.objects(Q(title = cardTitle) & Q(owner_name = session['user']['userName']))
        
        if(cardsList):
            cards = cardsList[0].cards
            if len(cards) > cardNumber:
                card = cards[cardNumber]
                # Remove card from cards list.
                CardsList.objects(Q(title = cardTitle) & Q(owner_name = session['user']['userName'])).update_one(pull__cards = card)

        return redirect('/editCardsList/'+ cardTitle)

    # Edit a cards list.
    def EditCards(self):
        # Set form variables.
        newTitle = request.form.get('title')
        oldTitle = request.form.get('oldTitle')
        newDescription = request.form.get('description')
        newPublic = True if request.form.get('public') == "true" else False
        
        cardsData = GetSingleCardsList(session['user']['userName'], oldTitle)

        # Edit description if changed.
        if(newDescription != cardsData['description']):
            CardsList.objects(Q(title = oldTitle) & Q(owner_name = session['user']['userName'])).update_one(set__description = newDescription)
        # Edit public if changed.
        if(newPublic != cardsData['public']):
            CardsList.objects(Q(title = oldTitle) & Q(owner_name = session['user']['userName'])).update_one(set__public = newPublic)
        # Edit title if changed.
        if(newTitle != oldTitle):
            # Check if title of cards already exits by owner.
            titleCheck = True if len(json.loads(CardsList.objects(Q(title = newTitle) & Q(owner_name = session['user']['userName'])).to_json())) == 0 else False
            if(titleCheck):
                CardsList.objects(Q(title = oldTitle) & Q(owner_name = session['user']['userName'])).update_one(set__title = newTitle)
            else:
                return jsonify({'error': 'Title already used.'}), 401
        
        return jsonify({'success': 'Sucess'}), 200

    # Edit a card from cards list.
    def EditCard(self):
        # Set form variables.
        questionEdit = request.form.get('questionEdit')
        answerEdit = request.form.get('answerEdit')
        cardsTitle = request.form.get('cardsTitle')
        cardIndex = int(request.form.get('cardIndex')) - 1

        if(questionEdit == '' or answerEdit == '' or cardsTitle == '' or cardIndex == ''):
            return jsonify({'success': 'Sucess'}), 200
        
        # Get cards, edit and save.
        cardsData = json.loads(CardsList.objects.get(title = cardsTitle).to_json())
        cards = cardsData['cards']
        cards[cardIndex] = {'question':questionEdit, 'answer': answerEdit}
        CardsList.objects(title = cardsTitle).update_one(set__cards = cards)

        return jsonify({'success': 'Sucess'}), 200

    # Edit UserName of a CardsUser.
    def EditName(self):
        formName = request.form.get('userName')

        # No change to name check.
        if(formName == session['user']['userName']):
            return jsonify({'error': 'No Change to userName'}), 400

        # Unique username check.
        nameExitsCheck = CardsUser.objects(userName = formName)
        if(nameExitsCheck):
            return jsonify({'error': 'UserName Already Exits'}), 400

        # Check form name Length.
        if(len(formName) < 1 or len(formName) > 32):
                return jsonify({"error": "userName needs to be 1-32 characters"}), 400

        CardsUser.objects(userName = session['user']['userName']).update_one(set__userName = formName)

        # Update owner name of cards to new name.
        CardsList.objects(owner_name = session['user']['userName']).update(set__owner_name = formName)

        # Update session var with name.
        session.modified = True
        session['user']['userName'] = formName

        return jsonify({"success": 'Sucess'}), 200

    # Edit Email of a CardsUser.
    def EditEmail(self):
        formEmail = request.form.get('email')

        # No change to name check.
        if(formEmail == session['user']['email']):
            return jsonify({'error': 'No Change to Email'}), 400

        # Unique email check.
        emailExitsCheck = CardsUser.objects(email = formEmail)
        if(emailExitsCheck):
            return jsonify({'error': 'Email Already Exits'}), 400

        # Check form email Length.
        if(len(formEmail) < 1 or len(formEmail) > 32):
                return jsonify({"error": "Email needs to be 1-32 characters"}), 400

        CardsUser.objects(email = session['user']['email']).update_one(set__email = formEmail)

        # Update session var with name.
        session.modified = True
        session['user']['email'] = formEmail

        return jsonify({'success': 'Sucess'}), 200
    
    # Edit password of cardUser.
    def EditPassword(self):
        oldPassword = request.form.get('password')
        newPassword = request.form.get('newPassword')
        newPasswordAgain = request.form.get('newPasswordAgain')
        
        user = CardsUser.objects.get(userName = session['user']['userName'])

        # Check if password matches.
        if not (pbkdf2_sha256.verify(oldPassword, user['password'])): 
            return jsonify({'error': 'Wrong password entered'}), 400

        # Check if new password is right length.
        if(len(newPassword) <=0 or len(newPassword) > 32):
            return jsonify({'error': 'New Password needs to be 0-32 characters.'}), 400

        # Check if new password matches re-entered new password.
        if(newPassword != newPasswordAgain):
            return jsonify({'error': 'Re-entered Password does not match New password.'}), 400

        # Edit password with new one.
        encrypted_password = pbkdf2_sha256.encrypt(newPassword)
        CardsUser.objects(userName = session['user']['userName']).update_one(set__password=encrypted_password)

        return jsonify({'success': 'Success'}), 200

# Get a users Cards. Sorted by timestamp.
def GetUsersCardsLists(userName):
    usersCards = json.loads(CardsList.objects(owner_name = userName).order_by('-timestamp').to_json())
    return usersCards

# Get a single cards list.
def GetSingleCardsList(userName, cardsTitle):
    cardsList = json.loads(CardsList.objects(Q(title = cardsTitle) & Q(owner_name = userName)).to_json())
    return cardsList[0]
        
# Get all public flash card sets sorted by timestamp.
def GetPublicCards():
        publicCards = json.loads(CardsList.objects(public = True).order_by('-timestamp').to_json())
        return publicCards

# Get a list of cards based on search of titles.
def GetCardsByTitleSearch():
    cardTitle = request.form.get('title')
    cardsList= json.loads( CardsList.objects(Q(public = True) & Q(title__contains = cardTitle)).to_json())
    #Check if list exits and return empty one if not.
    if(cardsList):
        return cardsList
    else:
        return []