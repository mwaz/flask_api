"""Class to deal with user authenticatication
"""
from app.helpers.decorators import token_required
from app.models import User, Sessions
from flask import request, jsonify, make_response
from flask.views import MethodView
from app import db
from app.helpers.auth_validators import user_registration_validation, \
    user_login_validation, password_reset_validation


class RegisterUser(MethodView):
    """ The class registers a new user
    """
    def post(self):
        """Method to handle post requests from the auth/register endpoint
        ---
        tags:
            - Auth
        parameters:
            - in: body
              name: User Register
              description: User's email, username and password
              required: true
              type: string
              schema:
                  id: register
                  properties:
                    email:
                      type: string
                      default: test@example.com
                    password:
                        type: string
                        default: P@ssword1
                    username:
                        type: string
                        default: User
                    secret_word:
                        type: string
                        default: TOP_SECRET
        responses:
            200:
              schema:
                  id: register
            422:
              description: Kindly Provide all required details
            400:
              description: Bad Requests
            """

        try:
            user_details = User.query.filter_by(
                email=request.data['email'].lower()).first()

            if not user_details:
                email = str(request.data.get('email', ''))
                password = str(request.data.get('password', ''))
                username = str(request.data.get('username', ''))
                secret = str(request.data.get('secret_word', ''))
                try:
                    user_registration_validation(email, username, password, secret)

                    user = User(email=email, password=password,
                                username=username, secret_word=secret)
                    user.save()
                    response = {'message': "Successfully registered"}
                    return make_response(jsonify(response)), 201

                except Exception as e:
                    response = {'message': str(e)}
                    return make_response(jsonify(response)), 400
            else:
                response = {'message': "User Exists, Kindly Login"}
                return make_response(jsonify(response)), 409
        except Exception:
            response = {"messsage": "Error occurred on creating User"}
            return make_response(jsonify(response)), 400


class LoginUser(MethodView):
    """Class to login a user from the ...auth/login endpoint
    """
    def post(self):
        """Method to Login a user
        ---
        tags:
            - Auth
        parameters:
            - in: body
              name: User Login
              description: User's email and password
              required: true
              type: string
              schema:
                id: login
                properties:
                  email:
                    type: string
                    default: test@example.com
                  password:
                    type: string
                    default: P@ssword1
        responses:
         200:
          schema:
            id: login
         401:
            description: Invalid Login Details
         422:
            description: Kindly Provide email and password
         400:
            description: Bad Requests
        """
        try:
            email = request.data['email']
            password = request.data['password']
            user_details = User.query.filter(email=email).first()
            user_login_validation(email, password)

            if user_details and user_details.password_check(password):
                access_token = user_details.user_token_generator(user_details.id)

                if access_token:
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
            response = {'message': 'Error occurred on user login'}
            return make_response(jsonify(response)), 400


class ResetUserPassword(MethodView):
    """Class to allow user to reset password
    """
    methods = ['PUT']

    def put(self):
        """Method to reset a password
        ---
        swagger: 2.0
        tags:
          - Auth
        parameters:
          - in: body
            name: Password Reset
            description: User's email and password
            required: true
            type: string
            schema:
              id: password_reset
              properties:
                email:
                  type: string
                  default: test@example.com
                reset_password:
                  type: string
                  default: new_P@@sword
                secret_word:
                  type: string
                  default: TOP_SECRET
        responses:
          200:
            schema:
              id: password_reset
          400:
            description: No password provided
          404:
            description: "Kindly provide correct email and secret word"
        """

        try:
            email = str(request.data.get('email', ''))
            user_details = User.query.filter_by(
                email=email).first()
            reset_password = str(request.data.get('reset_password', ''))
            secret_word = str(request.data.get('secret_word', ''))
            password_reset_validation(email, reset_password, secret_word)

            if user_details and user_details.secret_word_check(secret_word):
                res_password = User.password_hash(reset_password)
                user_details.password = res_password
                user_details.save()
                response = jsonify({'id': user_details.id,
                                    'email': user_details.email,
                                    'status': 'success',
                                   })
                return make_response(response), 200
            else:
                response = {"message": "Kindly provide correct email and secret word"}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400


class LogoutUser(MethodView):
    """Class to logout a particular user
    """
    methods = ['POST']
    decorators = [token_required]

    def post(self, current_user):
        """Method to call logout endpoint for a user
        ---
        tags:
          - Auth
        securityDefinitions:
          TokenHeader:
          type: apiKey
          name: Authorization
          description: Http Authentication
        security:
          - TokenHeader: []
        responses:
          200:
            description: Successfully logged out
          401:
            description: User not authenticated
          400:
            description: Bad Request

        """
        access_token = request.headers.get('Authorization')
        disable_token = Sessions(auth_token=access_token)
        db.session.add(disable_token)
        db.session.commit()
        response = jsonify({
            "message": "You logged out successfully.",
            "status": "success"
        })
        response.status_code = 200
        return response


user_password_reset_view = ResetUserPassword.as_view('user_password_reset_view')
user_registration_view = RegisterUser.as_view('user_registration_view')
user_login_view = LoginUser.as_view('user_login_view')
user_logout_view = LogoutUser.as_view('user_logout_view')
