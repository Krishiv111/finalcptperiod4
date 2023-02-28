""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Update(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    email = db.Column(db.String, unique=False)
    reviewtx = db.Column(db.String, unique=False)
    star = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, email, reviewtx, star):
        self.userID = id
        self.note = note
        self.email = email
        self.reviewtx = reviewtx
        self.star = star

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
       # file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "reviewtx": self.reviewtx,
            "star": self.star,
            "email":self.email,
           # "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class reviewadd(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=False, nullable=True)
    _star = db.Column(db.String(255), unique=False, nullable=False)
    _reviewtx = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Update", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, email, star, reviewtx):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._email = email
        self._star = star
        self._reviewtx = reviewtx

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
   
    @property
    def email(self):
       return self._email
  
    @email.setter
    def email(self, email):
       self._email = email


    def is_email(self, email):
       return self._email == email
    
    @property
    def star(self):
       return self._star
  
    @star.setter
    def star(self, star):
       self._star = star


    def is_star(self, star):
        return self._star == star
    
    @property
    def reviewtx(self):
       return self._reviewtx
  
    @reviewtx.setter
    def reviewtx(self, reviewtx):
       self._reviewtx = reviewtx


    def is_reviewtx(self, reviewtx):
       return self._reviewtx == reviewtx
  

    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "email": self.email,
            "star": self.star,
            "reviewtx": self.reviewtx,
          #  "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", email="", star="", reviewtx=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(email) > 0:
           self.email = email
        if len (star) > 0:
           self.star = star 
        if len(reviewtx) > 0:
           self.reviewtx = reviewtx    
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initreview():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        
        """Tester data for table"""
        r1 = reviewadd(name='Sam Johnson', uid='r1', email= 'Sam.johnson@gmail.com', star='three', reviewtx='The place was amazing and I really enjoyed it')
        r2 = reviewadd(name='Eric Middleton', uid='r2', email='Eric.Middleton@gmail.om', star='five', reviewtx='I wanted to stay longer and I really loved it. Thanks for the amazing Vac')
        r3 = reviewadd(name='Theo Fatless', uid='r3', email='Theo.Fatless@gmail.com', star='two', reviewtx='It was really nice but it was kinda hard to look though the website')
        r4 = reviewadd(name='Crunchy Mcfee ', uid='r4', email='Crunchy.Mcfee@gmail.com', star='three', reviewtx='It was good but I wanted a little more')
        r5 = reviewadd(name='Thicc Boi', uid='r5', email='Thicc.Boi@gmail.com', star='five', reviewtx='It satisfided me and I had a fun time')

        users = [r1, r2, r3, r4, r5]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                     note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Update(id=user.id, note=note, email=user._email, star=user._star, reviewtx=user._reviewtx, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            