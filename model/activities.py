'''
The below 7 lines import all of the modules necessary for the backend and backend/frontend connection. The especially important imports are the json, init, and sqlalchemy imports.
The "import json" import allows for the code in line 53, where the dump records are returned in json format, so that the python objects are readable in JSON format (text format). SQLAlchemy
is the database library being used to store all of the database info for this feature. Finally, the _init_ module is necessary, as it lets the interpreter know that there is Python code in a particular directory. 
In this case, there is Python code in the /api and /model directories.
'''

from random import randrange
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class ActivityDay(db.Model):
    __tableactivity__ = 'ActivityTime'  
    
    id = db.Column(db.Integer, primary_key=True)
    _activity = db.Column(db.String(255), nullable=False)
    _address = db.Column(db.String(255), nullable=False)
    _fun = db.Column(db.String(255), nullable=False )

    def __init__(self, activity, address, fun):
        self._activity = activity
        self._address = address
        self._fun = fun

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, activity):
       self._activity = activity

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
       self._address = address
    
    @property
    def fun(self):
        return self._fun
    
    @fun.setter
    def fun(self, fun):
       self._fun = fun

    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def read(self):
        return {
            "activity" : self.activity,
            "address" : self.address,
            "fun" : self.fun,
        }

def activity_table_empty():
    return len(db.session.query(ActivityDay).all()) == 0

def initActivity():
    db.create_all()
    #db.init_app(app)
    if not activity_table_empty():
        return
    
    a1 = ActivityDay('Daves Hot Chicken', '1268 Auto Park Way, Escondido, CA 92029', "8/10")
    a2 = ActivityDay('Raising Canes', '8223 Mira Mesa Blvd, San Diego, CA 92126', "10/10")
    a3 = ActivityDay('Belmont Park', '3146 Mission Blvd, San Diego, CA 92109', "7/10")
    a4 = ActivityDay('Potato Chip Rock', 'Ramona, CA 92065', "6/10") 
    
    activityslist = [a1, a2, a3, a4]

    for activity in activityslist:
        try:
            db.session.add(activity)
            db.session.commit()
        except IntegrityError as e:
            print("Error: " +str(e))
            '''fails with bad or duplicate data'''
            db.session.rollback()    