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

'''
The below is where the "ActivityDay" class is being defined. This contains all of the data for the feature that needs to be managed.
'''
class ActivityDay(db.Model):
    __tableactivity__ = 'ActivityTime'  
    
    '''
    The below sets all of the keys that are going to be looked at. The id key is special, as it is the primary key. This is what any sort of PUT and DELETE requests will be passed through if operable.
    '''
    id = db.Column(db.Integer, primary_key=True)
    _activity = db.Column(db.String(255), nullable=False)
    _address = db.Column(db.String(255), nullable=False)
    _fun = db.Column(db.String(255), nullable=False )
    
    '''
    This is constructing the activity object and the "_init_" portion is initializing the variables within that activity object. 
    In this case, this is the activity, address, and fun variables that are within this object.
    '''
    def __init__(self, activity, address, fun):
        self._activity = activity
        self._address = address
        self._fun = fun
    
    '''
    the following lines 44-75 contain the setter and getter methods. each of the three above variables (activity, address, fun)
    are being extracted from the object and then upaddressd after the object is created. 
    '''
    @property
    def activity(self):
        return self._activity
    
    # setting activity variable in object

    @activity.setter
    def activity(self, activity):
       self._activity = activity
    
    # extracting address from object
    @property
    def address(self):
        return self._address
    
    # setting address variable in object
    
    @address.setter
    def address(self, address):
       self._address = address
    
    # extracting fun from object
    
    @property
    def fun(self):
        return self._fun
    
    # setting fun variable in object
    
    @fun.setter
    def fun(self, fun):
       self._fun = fun
    
    '''
    The content is being outputted using "str(self)". It is being returned in JSON format, which is a readable format. This is a getter function.
    '''
    def __str__(self):
        return json.dumps(self.read())
    
    
    '''
    defining the create method. self allows us to access all of the attributes 
    of the current object. after the create method is defined, the data is queried from the DB.
    in this case, since it is the create method, the data is being ADDED, and then db.session.commit() is used
    to commit the DB transaction and apply the change to the DB.
    '''
    
    '''
    here, there is an integrity error "except" statement. db.session would be autocommitted 
    without the db.session.remove() line, and that's something we don't want for the purpose of the project.
    '''
    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    '''
    the delete method is defined with the "self" parameter. this method is mainly for certain instances in the DB being 
    garbage collected, and the object kills itself.
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    def update(self, activity="", address="", fun=""):
        """only updates values with length"""
        if len(activity) > 0:
           self.activity = activity
        if len (address) > 0:
           self.address = address 
        if len(fun) > 0:
           self.fun = fun    
        db.session.commit()
        return self

    '''
    read method with the self parameter, reading the object with all of the 
    properties: activity, address, and fun are being returned.
    '''
    def read(self):
        return {
            "activity" : self.activity,
            "address" : self.address,
            "fun" : self.fun,
        }

'''
handling the situation where the table is completely empty,
returns the length from the session query of the initialized class ActivityDay to be 0.
'''
def activity_table_empty():
    return len(db.session.query(ActivityDay).all()) == 0
'''
defines the initActivity function, and then creates the tables and the DB here through the db.create_all() method.
'''
def initActivity():
    db.create_all()
    #db.init_app(app)
    if not activity_table_empty():
        return
    
    a1 = ActivityDay('Daves Hot Chicken', '1268 Auto Park Way, Escondido, CA 92029', "8/10")
    a2 = ActivityDay('Raising Canes', '8223 Mira Mesa Blvd, San Diego, CA 92126', "10/10")
    a3 = ActivityDay('Belmont Park', '3146 Mission Blvd, San Diego, CA 92109', "7/10")
    a4 = ActivityDay('Potato Chip Rock', 'Ramona, CA 92065', "6/10") 
    
    '''
    the variable "activityslist" being used for the tester data, containing a1, a2, a3, and a4 the variables with the sample data above.
    '''
    activityslist = [a1, a2, a3, a4]
    
    
    '''
    the below is for the sample data: for each activity in the defined activitylist, the DB session will add that activity, and then commit the transaction
    with the next line. or, if there is bad/duplicate data, the data will not be committed, and session will be rolled back to its previous
    state. 
    '''

    for activity in activityslist:
        try:
            db.session.add(activity)
            db.session.commit()
        except IntegrityError as e:
            print("Error: " +str(e))
            '''fails with bad or duplicate data'''
            db.session.rollback()    