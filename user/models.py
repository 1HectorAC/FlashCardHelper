from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid
from mongoengine import connect, Document, StringField, ListField, DictField, BooleanField, DateTimeField
from mongoengine.queryset.visitor import Q
from datetime import datetime
import json
import os
import re

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
        formUserName = request.form.get('name')
        formEmail = request.form.get('email')
        formPassword = request.form.get('password')
        formPasswordAgain = request.form.get('passwordAgain')

        # INPUT VALIDATION
        # Input length also checked in html so this is not likely used, but still important just in case.
        if len(formUserName) <=0 or len(formPassword) < 4:
            return jsonify({'error': 'Input(s) too short.'}), 400
        if len(formUserName) >16 or len(formPassword) >= 32:
            return jsonify({'error': 'Input(s) too long.'}), 400
        # Email format check.
        emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(not re.search(emailRegex,formEmail)):   
            return jsonify({"error": "Email is not properly formated."}), 400
        # Password and re-entered password match check.
        if formPassword != formPasswordAgain:
            return jsonify({'error':'Password and Re-Entered Password don\'t match.'}), 400    
        # Unique username check.
        nameExitsCheck = CardsUser.objects(userName = formUserName)
        if(nameExitsCheck):
            return jsonify({'error': 'Signup failed. UserName Already Exits'}), 400
        # Unique email check.
        emailExitsCheck = CardsUser.objects(email = formEmail)
        if(emailExitsCheck):
            return jsonify({'error': 'Signup failed. Email Already Exits'}), 400

        #Create user object.
        user = CardsUser(
            _id = uuid.uuid4().hex,
            userName = formUserName,
            email = formEmail,
            password = formPassword
        )

        # Encrypt password
        user.password = pbkdf2_sha256.encrypt(user['password'])

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
        formTitle = request.form.get('title')
        formDescription = request.form.get('description')
        formPublic = request.form.get('public')
        cards = GetUsersCardsLists(session['user']['userName'])

        # INPUT VALIDATION
        # Input length also checked in html so this is not likely used, but still important just in case.
        if len(formTitle) <= 0 or len(formDescription) <= 0:
            return jsonify({'error':'Inputs can\'t be empty.'}), 400
        if len(formTitle) > 16 or len(formDescription) > 100:
            return jsonify({'error': 'Inputs are too long.'}),400
        # check if hit max number of flash card sets limit.
        if len(cards) > 50:
            return jsonify({'error':'Max Flash Cards limit is 50. Delete some to make more.'}), 400
        
        # Get person to save owner reference into into cardsList created.
        person = CardsUser.objects.get(email = session['user']['email'])

        cards = CardsList(
            _id = uuid.uuid4().hex,
            title = formTitle,
            description = formDescription,
            public = True if formPublic == "true" else False,
            cards = [],
            owner_name = person.userName  
        )
        if cards.save():
            return jsonify({"success": "Sucess"}), 200

        return jsonify({'error':'Invalid cards.'}), 400

    # Delete Cards list.
    def RemoveCardsList(self, cardTitle):
        # Get cards list of given title that is owned by the user
        cardsList = CardsList.objects(Q(title = cardTitle) & Q(owner_name = session['user']['userName']))
        
        # Delete object if exits.
        if(cardsList):
          cardsList.delete()

        return redirect('/dashboard/')

    # Add a card to cards list.
    def addCard(self):
        questionList = request.form.getlist('questionPart')
        answerList = request.form.getlist('answerPart')
        cardsTitle = request.form.get('cardsTitle')
        
        # INPUT VALIDATION
        # Input length also checked in html so this is not likely used, but still important just in case.
        if len(questionList) <=0 or len(answerList) < 0:
            return jsonify({'error': 'Empty Questions or Answers'}),400
        if len(questionList) > 20 or len(answerList) > 20:
            return jsonify({'error': 'To many Questions or Answers'}), 400

        # Check if max cards limit reached.
        cards = GetSingleCardsList(session['user']['userName'], cardsTitle)
        if len(cards) + len(questionList) > 150:
            return jsonify({'error':'150 cards Limit. Make less cards or delete some.'}), 400

        # Setup data to add.
        data = []
        if "" not in questionList and "" not in answerList and len(questionList) == len(answerList):
            for x in range(0, len(questionList)):
                if len(answerList[x]) > 100 or len(questionList[x]) > 100:
                    return jsonify({'error':'A Question/Answer is longer than 100 characters.'}),400
                data.append({'question' : questionList[x], 'answer' : answerList[x]})
        else:
            return jsonify({'error':'There is an emply question or answer.'}), 400
        
        # Added cards to cardslist
        if CardsList.objects(Q(title = cardsTitle) & Q(owner_name = session['user']['userName'])).update_one(push_all__cards = data):
            return jsonify({"success": "Sucess"}), 200
            
        return jsonify({'error':'Invalid cards.'})

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
            # Description length validcation.
            if len(newDescription) <=0 or len(newDescription) > 100:
                return jsonify({'error': 'Description must be between 1-100 characters.'}),400
            CardsList.objects(Q(title = oldTitle) & Q(owner_name = session['user']['userName'])).update_one(set__description = newDescription)
        
        # Edit public if changed.
        if(newPublic != cardsData['public']):
            CardsList.objects(Q(title = oldTitle) & Q(owner_name = session['user']['userName'])).update_one(set__public = newPublic)
        
        # Edit title if changed.
        if(newTitle != oldTitle):
            # Title length validation.
            if len(newTitle) <=0 or len(newTitle) > 16:
                return jsonify({'error':'Title must be between 1-16 characters.'}),400
            # Check if title of cards already exits by owner.
            titleCheck = True if len(json.loads(CardsList.objects(Q(title = newTitle) & Q(owner_name = session['user']['userName'])).to_json())) == 0 else False
            if(titleCheck):
                CardsList.objects(Q(title = oldTitle) & Q(owner_name = session['user']['userName'])).update_one(set__title = newTitle)
            else:
                return jsonify({'error': 'Title already used.'}), 400
        
        return jsonify({'success': 'Sucess'}), 200

    # Edit a card from cards list.
    def EditCard(self):
        # Set form variables.
        questionEdit = request.form.get('questionEdit')
        answerEdit = request.form.get('answerEdit')
        cardsTitle = request.form.get('cardsTitle')
        cardIndex = int(request.form.get('cardIndex')) - 1

        #VALICATION
        # Length and empty data already checked in html. This is just for extra security.
        if questionEdit == '' or answerEdit == '' or cardsTitle == '' or cardIndex == '':
            return jsonify({'error': 'Empty data submited'}), 400
        if len(questionEdit) > 100 or len(answerEdit) > 100:
            return jsonify({'error': '100 Char limit.'}), 400
        
        # Get cards, edit and save.
        cardsData = json.loads(CardsList.objects.get(title = cardsTitle).to_json())
        cards = cardsData['cards']
        cards[cardIndex] = {'question':questionEdit, 'answer': answerEdit}

        if CardsList.objects(title = cardsTitle).update_one(set__cards = cards):
            return jsonify({'success':'Sucess'}),200

        return jsonify({'error': 'Invalid edit card data'}), 400

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
        if(len(formName) < 1 or len(formName) > 16):
                return jsonify({"error": "userName needs to be 1-16 characters"}), 400

        if CardsUser.objects(userName = session['user']['userName']).update_one(set__userName = formName):
            CardsList.objects(owner_name = session['user']['userName']).update(set__owner_name = formName)
            
            # Update session var with name.
            session.modified = True
            session['user']['userName'] = formName

            return jsonify({"success": 'Sucess'}), 200

        return jsonify({'error':'Error Changing Name'})

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