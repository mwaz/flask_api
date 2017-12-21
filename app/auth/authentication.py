""""Class to deal with user authenticatication
"""
from app.decorators import token_required
from app.models import User, Sessions
from flask import request, jsonify, abort, make_response
from flask.views import MethodView
from app import db


class userRegister(MethodView):
    """" The class registers a new user
    """

    def post(self):
        """Method to handle post requests from the auth/register endpoint
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
                  properties:
                    email: 
                      type: string
                      default: test@example.com
                    password:
                        type: string
                        default: P@ssword1
            401:
              description: Invalid Login Details
            422:
              description: Kindly Provide email and password
            400:
              description: Bad Request
            
            """

        user_details = User.query.filter_by(
            email=request.data['email']).first()
        if not user_details:
            try:
                email = str(request.data.get('email', ''))
                password = str(request.data.get('password', ''))

                if not email or not password:
                    response = {'message': "Kindly Provide email and password"}
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
    """"Class to login a user from the ...auth/login endpoint
    """
    
    def post(self):
        """"Method to Login a user
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
          properties:
            email: 
              type: string
              default: test@example.com
            password:
              type: string
              default: P@ssword1
        401:
            description: Invalid Login Details
        422:
            description: Kindly Provide email and password
        400:
            description: Bad Request
            
        """
        try:
            email=request.data['email']
            password = request.data['password']
            user_details = User.query.filter_by(email=email).first()

            if not email or not password:
                response = {'message': "Kindly Provide email and password"}
                return make_response(jsonify(response)), 422

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
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400

class userPasswordReset(MethodView):
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
        responses:
          200:
            schema:
              id: password_reset
              properties:
                email:
                  type: string
                  default: test@example.com
                reset_password:
                  type: string
                  default: new_P@@sword
          400:
            description: No password provided
          404:
            description: Email not found
        """

        try:
            user_details= User.query.filter_by(email=request.data['email']).first()
            reset_password = str(request.data.get('reset_password', ''))
            if not reset_password:
                response = {"message": "No password provided"}
                return make_response(jsonify(response)), 400
            if user_details:
                res_password = User.password_hash(reset_password)
                user_details.password = res_password
                user_details.save()
                response = jsonify({
                            'id': user_details.id,
                            'email': user_details.email,
                            'status': 'success',
                        })
                return make_response(response), 200
            else:
                response = {"message": "Email not found"}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400

class userLogout(MethodView):
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

user_password_reset_view = userPasswordReset.as_view('user_password_reset_view')
user_registration_view = userRegister.as_view('user_registration_view')
user_login_view = userLogin.as_view('user_login_view')
user_logout_view = userLogout.as_view('user_logout_view')
