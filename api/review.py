import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.reviewers import reviewadd

# Change variable name and API name and prefix
review_api = Blueprint('review_api', __name__,
                   url_prefix='/api/reviews')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(review_api)

class ReviewAPI:     
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            # validate uid

            email = body.get('')
            if email is None or len(email) < 0:
                return {'message': f'email is missing, or is less than 2 characters'}, 210
            reviewtx = body.get('reviewtx')
            if reviewtx is None or len(reviewtx) < 1:
                return {'message': f'review is missing, or is less than 2 characters'}, 210
            star = body.get('star')
            if star is None or len(star) < 1:
                return {'message': f'star is missing, or is less than 2 characters'}, 210
            

            ''' #1: Key code block, setup USER OBJECT '''
            uo = reviewadd(name=name, email=email, reviewtx=reviewtx, star=star)
            
            ''' Additional garbage error checking '''
            # set password if provided
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            review = uo.create()
            # success returns json of user
            if review:
                return jsonify(review.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            users = reviewadd.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            
            
            ''' Find user '''
            
            
            ''' authenticated user '''
            

            

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Security, '/authenticate')
