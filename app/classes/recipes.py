"""Class to handle creation  and manipulation of recipe categories"""
from app.models import Recipes
from app.models import User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView

class Recipe(MethodView):
    """"Class to define get and post requests of recipes"""
    methods = ['GET', 'POST']

    def post(self, category_id):
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category_id = Recipes.query.filter_by(category_id=category_id)
                if category_id:
                    recipe_name = str(request.data.get('recipe_name', ''))
                    recipe_ingredients = request.data.get('recipe_ingredients', '')
                    recipe_methods = request.data.get('recipe_methods', '')
                    if recipe_name:
                        recipe = Recipes(recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                                         recipe_methods=recipe_methods, category_id=category_id)
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
                response = {'message': 'Category name does not exist'}
                response = make_response(jsonify(response)), 404
                return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401

    def get(self, category_id):
        """"Method to retrieve all the recipes that belong to a category"""
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipes = Recipes.query.filter_by(category_id=category_id)
                for recipe in recipes:
                    recipe_obj = {'id': recipe.id,
                                  'recipe_name': recipe.recipe_name,
                                  'recipe_ingredients': recipe.recipe_ingredients,
                                  'recipe_methods': recipe.recipe_methods,
                                  'category_name': recipe.category_name,
                                  'date_created': recipe.date_created,
                                  'date_modified': recipe.date_modified
                                  }

                    response = make_response(jsonify(recipe_obj)), 200
                    return response
            response = {'message': 'User not authenticated'}
            return make_response(jsonify(response)), 401


recipe_post_get_view = Recipe.as_view('recipe_post_get_view')

