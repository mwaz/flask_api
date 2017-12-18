import jwt
from flask import jsonify, make_response, request
from functools import wraps
from app.models import User, Sessions


def token_required(f):
    """Decorator to check if user is logged in
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        authorization_header = request.headers.get('Authorization')      
        if authorization_header:
            access_token = authorization_header
        if not access_token:
            response = {"message": "User is not authenticated"}
            return make_response(jsonify(response)), 401
        blacklisted_token = Sessions.check_logout_status(access_token)
        if blacklisted_token:
            return make_response(jsonify({"message":"User is already logged out, Please login"}), 401)
        else:
            current_user = User.query.filter_by(id=User.decode_token(access_token)).first()        
        return f(current_user, *args, **kwargs)
    return decorated
