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

class userLogin(MethodView):
    """"Class to login a user from the ...auth/login endpoint"""
    def post(self):
        """"Method to check user login via a POST request"""

        try:
            user_details = User.query.filter_by(email=request.data['email']).first()
            password = request.data['password']
            if user_details and user_details.password_check(password):
                granted_access_token = user_details.user_token_generator(user_details.id)
                if granted_access_token:
                    response = {
                        'message': 'Successful Login',
                        'access_token': granted_access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid Login Details'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500



user_registration_view = userRegister.as_view('user_registration_view')
user_login_view = userRegister.as_view('user_login_view')



