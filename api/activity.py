from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse # used for REST API building
# the class ActivityDay, defined in the corresponding model file for the feature, is being imported for its usage in the api.
from model.activities import ActivityDay

activities_api = Blueprint('activities_api', __name__, url_prefix='/api/activities')

api = Api(activities_api)

class activitiesAPI:
     
    class _Create(Resource):
        def post(self):

             body = request.json
             
             activities = body.get('activities')
             if activities is None or len(activities) < 3:
                return {'message': f'activities is missing'}, 210
           
             address = body.get('address')
             fun = body.get('fun')

             uo = ActivityDay(activities, address, fun)
           
             activities = uo.create()

             if activities:
                return jsonify(activities.read())

             return {'message': f'Processed activities error'}, 210
       
    class _Read(Resource):
        def get(self):
            activities = ActivityDay.query.all()    
            json_ready = [activities.read() for activities in activities]  
            return jsonify(json_ready)  
        

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')