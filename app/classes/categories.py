"""Class to handle category creation, viewing and manipulation"""
from app.models import Categories, User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView
import re


class Category(MethodView):
    methods = ['GET', 'POST']
    # @app.route('/flask_api/v1/categories/', methods=['POST'])
    def post(self):
        """"Method to add a new category to the endpoint"""
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        regex_pattern = "[a-zA-Z- .]+$"

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category_name = str(request.data.get('category_name', ''))
                
                if not category_name:
                    response = {'message': 'category name not provided'}
                    return make_response(jsonify(response)), 400

                if not re.search(regex_pattern, category_name):
                    response = {'message': 'Category name is not valid'}
                    return make_response(jsonify(response)), 400 

                if category_name:  
                    category_name = re.sub(r'\s+', ' ', category_name).strip()
                    category_name = None if category_name == " " else category_name.title()
                    category_details = Categories.query.filter_by(category_name=category_name,created_by=user_id).first()
                
                    if category_details:
                        response = {'message': 'Category name exists'}
                        return make_response(jsonify(response)), 400 

                    category = Categories(category_name=category_name,created_by=user_id)
                    category.save()
                    response = jsonify({
                        'id': category.id,
                        'category_name': category.category_name,
                        'created_by': category.created_by,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    })
                    response.status_code = 201
                    return response
                else:
                    response = {'message': 'not created'}
                    response = jsonify(response)
                    response.status_code = 401
                    return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401


    # @app.route('/flask_api/v1/categories/', methods=['GET'])
    def get(self):
        """"Method to get all categories"""
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                categories = Categories.get_all_user_categories()
                results = []
                for category in categories:
                    category_object = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    }
                    results.append(category_object)
                response = jsonify(results)
                response.status_code = 200
                return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401

class CategoriesManipulation(MethodView):
    """Class to handle manipulation of categories using PUT, POST, DELETE and GER"""
    methods = ['GET','POST', 'PUT', 'DELETE']
    def get(self, id):
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Categories.query.filter_by(id=id).first()
                if category:
                    response = jsonify({
                        'id': category.id,
                        'category_name': category.category_name,
                        'created_by': category.created_by,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    })
                    response.status_code = 200
                    return response
                else:
                    response = {'message': 'No Category Found'}
                    return make_response(jsonify(response)), 404
                
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401

    def put(self, id):
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        regex_pattern = "[a-zA-Z- .]+$"
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Categories.query.filter_by(id=id).first()
                category_name = str(request.data.get('category_name', ''))
                
                if not category_name:
                    response = {'message': 'category name not provided'}
                    return make_response(jsonify(response)), 400

                if not re.search(regex_pattern, category_name):
                    response = {'message': 'Category name is not valid'}
                    return make_response(jsonify(response)), 400 
                
                if not category:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)
                else:
                    category_name = re.sub(r'\s+', ' ', category_name).strip()
                    category_name = None if category_name == " " else category_name.title()
                    category_details = Categories.query.filter_by(category_name=category_name,created_by=user_id).first()
                
                    if category_details:
                        response = {'message': 'Category name exists'}
                        return make_response(jsonify(response)), 400 

                    category.category_name = category_name
                    category.save()
                    response = jsonify({
                        'id': category.id,
                        'category_name': category.category_name,
                        'created_by': category.created_by,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    })
                    response.status_code = 200
                    return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401

    def delete(self, id):
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Categories.query.filter_by(id=id).first()
                if not category:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)
                else:
                   category.delete_categories()
                   return {
                            "message": "successfully deleted category".format(category.id)
                          }, 200
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401


category_view_post = Category.as_view('category_view_post')

category_manipulation = CategoriesManipulation.as_view('category_manipulation')