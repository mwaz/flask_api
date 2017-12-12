"""Class to handle creation  and manipulation of recipe categories"""
from app.models import Recipes, Categories
from app.models import User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView
import re

class Recipe(MethodView):
    """"Class to define get and post requests of recipes"""
    methods = ['GET', 'POST']

    def post(self, id):
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        regex_pattern = "[a-zA-Z- .]+$"

        if access_token:
            user_id = User.decode_token(access_token)
            category_id = id
            if not isinstance(user_id, str):
                # category_id = Categories.query.filter_by(id=category_id).first()
                # category_id = Recipes.query.filter_by(category_id=category_id).firs

                if category_id:
                    recipe_name = str(request.data.get('recipe_name', ''))
                    recipe_ingredients = request.data.get('recipe_ingredients', '')
                    recipe_methods = request.data.get('recipe_methods', '')
                    # category_id = request.data.get('category_id', '')
        
                    if not recipe_name :
                        response = {'message': 'Recipe name not provided'}
                        return make_response(jsonify(response)), 400
                    if not recipe_ingredients :
                        response = {'message': 'Recipe ingredients not provided'}
                        return make_response(jsonify(response)), 400
                    if not recipe_methods :
                        response = {'message': 'Recipe preparation methods not provided'}
                        return make_response(jsonify(response)), 400

                    if not re.search(regex_pattern, recipe_name):
                        response = {'message': 'Recipe name is not valid'}
                        return make_response(jsonify(response)), 400 


                    if recipe_name:
                        recipe_name = re.sub(r'\s+', ' ', recipe_name).strip()
                        recipe_name = None if recipe_name == " " else recipe_name.title()
                        recipe = Recipes(recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                                         recipe_methods=recipe_methods, category_id=category_id)
                        recipe_details = Recipes.query.filter_by(category_id=category_id,recipe_name=recipe_name).first()
                
                        if recipe_details:
                            response = {'message': 'Recipe name exists'}
                            return make_response(jsonify(response)), 400 
                        recipe.save()
                        response = {'id':recipe.id,
                                    'recipe_name': recipe.recipe_name,
                                    'recipe_ingredients': recipe.recipe_ingredients,
                                    'recipe_methods': recipe.recipe_methods,
                                    'category_id': recipe.category_id,
                                    'date_created': recipe.date_created,
                                    'date_modified': recipe.date_modified
                                    }
                        response = make_response(jsonify(response)),201
                        return response
                    else:
                        response = {'message': 'unable to create recipe'}
                        response = make_response(jsonify(response)), 401
                        return response
                response = {'message': 'Category does not exist'}
                response = make_response(jsonify(response)), 404
                return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401

    def get(self, id):
        """"Method to retrieve all the recipes that belong to a category"""
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            category_id = id
            if not isinstance(user_id, str):
                recipes = Recipes.get_all_user_recipes(category_id)
                results = []
                for recipe in recipes:
                    recipe_obj = {'id': recipe.id,
                                  'recipe_name': recipe.recipe_name,
                                  'recipe_ingredients': recipe.recipe_ingredients,
                                  'recipe_methods': recipe.recipe_methods,
                                  'category_id': recipe.category_id,
                                  'date_created': recipe.date_created,
                                  'date_modified': recipe.date_modified
                                  }
                    results.append(recipe_obj)
                response = jsonify(results)
                response.status_code = 200
                return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401

class recipes_manipulation(MethodView):
    """Class to handle GET, PUT and DELETE for individual recipes in a category"""
    methods = ['GET','POST', 'PUT', 'DELETE']
    def get(self, id, recipe_id):
        """Method to get a specific recipe in a category """
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe = Recipes.query.filter_by(category_id=id, id=recipe_id ).first()
                if not recipe:
                    response = {'message':'No recipe found'}
                    response = make_response(jsonify(response)), 404
                    return response
                else:
                    response = {'id': recipe.id,
                                'recipe_name': recipe.recipe_name,
                                'recipe_ingredients': recipe.recipe_ingredients,
                                'recipe_methods': recipe.recipe_methods,
                                'category_id': recipe.category_id,
                                'date_created': recipe.date_created,
                                'date_modified': recipe.date_modified
                                }
                    response = make_response(jsonify(response)), 201
                    return response

    def put(self,  id, recipe_id):
        """Method to edit a recipe in a category"""

        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]
        regex_pattern = "[a-zA-Z- .]+$"
        category_id = id

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe = Recipes.query.filter_by(category_id=category_id, id=recipe_id).first()
                recipe_name = str(request.data.get('recipe_name', ''))
                recipe_ingredients = str(request.data.get('recipe_ingredients', ''))
                recipe_methods = str(request.data.get('recipe_methods', ''))
                   
                if not recipe_name :
                    response = {'message': 'Recipe name not provided'}
                    return make_response(jsonify(response)), 400
                if not recipe_ingredients :
                    response = {'message': 'Recipe ingredients not provided'}
                    return make_response(jsonify(response)), 400
                if not recipe_methods :
                    response = {'message': 'Recipe preparation methods not provided'}
                    return make_response(jsonify(response)), 400

                if not re.search(regex_pattern, recipe_name):
                    response = {'message': 'Recipe name is not valid'}
                    return make_response(jsonify(response)), 400 

                if not recipe:
                    response = {'message': 'No recipe found'}
                    response = make_response(jsonify(response)), 404
                    return response
                else:
                    recipe_name = re.sub(r'\s+', ' ', recipe_name).strip()
                    recipe_name = None if recipe_name == " " else recipe_name.title()     
                    recipe.recipe_name = recipe_name
                    recipe.recipe_ingredients = recipe_ingredients
                    recipe.recipe_methods = recipe_methods
                    recipe.save()
                    response = {'id': recipe.id,
                                'recipe_name': recipe.recipe_name,
                                'recipe_ingredients': recipe.recipe_ingredients,
                                'recipe_methods': recipe.recipe_methods,
                                'category_id': recipe.category_id,
                                'date_created': recipe.date_created,
                                'date_modified': recipe.date_modified
                                }
                    response = make_response(jsonify(response)), 201
                    return response

    def delete(self,  id, recipe_id):
        """Method to delete a recipe in a category"""

        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe = Recipes.query.filter_by(category_id=id,id=recipe_id).first()
                if not recipe:
                    response = {'message': 'No recipe found'}
                    response = make_response(jsonify(response)), 401
                    return response
                else:
                    recipe.delete_recipes()
                    response ={"message": "successfully deleted category".format(recipe.id)}
                    response = make_response(jsonify(response)), 200
                    return response

recipe_post_get_view = Recipe.as_view('recipe_post_get_view')
recipe_manipulation_view = recipes_manipulation.as_view('recipe_manipulation_view')

