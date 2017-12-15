""""Class to deal with user authenticatication"""
from app.models import User, Sessions
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
                email = str(request.data.get('email', ''))
                password = str(request.data.get('password', ''))
                
                if not email and not paassord:
                    response = {'message': "No email provided"}
                    return make_response(jsonify(response)), 422

                user = User(email=email, password=password)
                user.save()
                response = {'message': "Successfully registered"}
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 400
        else:
            response = {'message': "User Exists, Kindly Login"}
            return make_response(jsonify(response)), 409

class userLogin(MethodView):
    """"Class to login a user from the ...auth/login endpoint"""
    def post(self):
        """"Method to check user login via a POST request"""

        try:
            user_details = User.query.filter_by(email=request.data['email']).first()
            password = request.data['password']
            if user_details and user_details.password_check(password):
                access_token = user_details.user_token_generator(user_details.id)
                session = Session.login(user_details.id)
                if access_token and session:
                    response = {
                        'message': 'Successful Login',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid Login Details'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400

class userPasswordReset(MethodView):
    """Class to allow user to reset password
    """
    def put(self):
        """Method to reset a password
        """
        methods=['PUT']
        try: 
            user_details= User.query.filter_by(email=request.data['email']).first()
            reset_password = str(request.data.get('reset_password', ''))
            if user_details:
                res_password = User.password_hash(reset_password)
                user_details.password = res_password
                user_details.save()
                response = jsonify({
                            'id': user_details.id,
                            'email': user_details.email,
                        })
                return make_response(response), 200
            else:
                response = {"message": "Email not found"}
                return make_response(jsonify(response)), 404
        except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 400








user_password_reset_view = userPasswordReset.as_view('user_password_reset_view')
user_registration_view = userRegister.as_view('user_registration_view')
user_login_view = userLogin.as_view('user_login_view')




