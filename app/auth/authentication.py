""""Class to deal with user authenticatication"""
from app.models import User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView


class userRegister(MethodView):
    """" The class registers a new user"""

    def post(self):
        """"Method to handle post requests from the auth/register endpoint"""

        #check if a particular user exists
        user_details = User.query.filter_by(email=request.data['email']).first()
        if not user_details:
            try:
                email = request.data['email']
                password = request.data['password']
                user = User(email=email, password=password)
                user.save()
                response = {'message': "Successfully registered"}
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 401
        else:
            response = {'message': "User Exists, Kindly Login"}
            return make_response(jsonify(response)), 202

user_registration_view = userRegister.as_view('user_registration_view')



