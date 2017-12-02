from app.models import Recipes
from app.models import User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView

class Recipe(MethodView):
    """"Class to define get and post requests of recipes"""
    methods = ['GET', 'POST']

    def post(self, category_name):
        category_name = Recipes.query.filter_by(category_id=category_name)
        if category_name:
            recipe_name = str(request.data.get('recipe_name', ''))
            recipe_ingredients = request.data('recipe_ingredients')
            recipe_methods = request.data('recipe_methods')
            if recipe_name:
                recipe = Recipes(recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                                 recipe_methods=recipe_methods)
                recipe.save()
                response = {'id':recipe.id,
                            'recipe_name': recipe.recipe_name,
                            'recipe_ingredients': recipe.recipe_ingredients,
                            'recipe_methods': recipe.recipe_methods,
                            'category_name': recipe.category_name,
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

    def get(self, category_id):
        """"Method to retrieve all the recipes that belong to a category"""
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

