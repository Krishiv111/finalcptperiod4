from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse # used for REST API building
# the class ActivityDay, defined in the corresponding model file for the feature, is being imported for its usage in the api.
from model.activities import ActivityDay

# this is where the blueprint class is defined and the url prefix is set, which is then registered to the app in the main.py file.
activities_api = Blueprint('activities_api', __name__, url_prefix='/api/activities')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activities_api)

# this is the main entry point for the app, with the class activitiesAPI. 
class activitiesAPI:
    # the _create class is being referred to for the post method, to post the objects.        
    class _Create(Resource):
        def post(self):
             ''' Read data for json body '''
             body = request.json
             
             ''' Avoid garbage in, error checking '''
            # valiaddress name
            
            # here, this handles error checking, as the shortest activities in the world is 3 characters, so if the activities is less than that, it is deemed invalid and not added to the DB.
             activities = body.get('activities')
             if activities is None or len(activities) < 3:
                return {'message': f'activities is missing'}, 210
           
            # look for address, fun variables
             address = body.get('address')
             fun = body.get('fun')


             # this sets up the activities object
             uo = ActivityDay(activities, address, fun)
           
           
             # this adds the activities to the DB (uo.create())
             activities = uo.create()
             
             # if the addition was successful, then the activities is returned to the user in a readable JSON format.
             if activities:
                return jsonify(activities.read())
            # failure returns error
             return {'message': f'Processed activities error'}, 210
    
    # _Read class, needed for the GET request.     
    class _Read(Resource):
        def get(self):
            activities = ActivityDay.query.all()    # read/extract all activities from database
            json_ready = [activities.read() for activities in activities]  # prepares the readable output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        


    # building the API endpoints. there is a create and read endpoint, to serve for both the GET and POST requests.
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')