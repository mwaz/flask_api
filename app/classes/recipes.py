"""Class to handle creation  and manipulation of recipe categories
"""

from app.decorators import token_required
from app.models import Recipes, Categories
from app.models import User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView
import re

class Recipe(MethodView):
    """"Class to define get and post requests of recipes
    """
    methods = ['GET', 'POST']
    decorators = [token_required]
    def post(self, current_user, id):
        """Method to add a recipe in a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []

        parameters:
            - in: body
              name: Recipe Register
              required: true
              type: string
              schema:
                id: recipes
                properties:
                  recipe_name:
                    type: string
                    default: Panckakes
                  recipe_ingredients:
                    type: long
                    default: Milk, Flour
                  recipe_methods:
                    type: long
                    default: Cook in a pan till ready
            - in: path
              name: id
              required: true
              type: integer



        responses:
          200:
            schema:
              id: recipes

        """
        regex_pattern = "[a-zA-Z- .]+$"
        category_id = id
        if category_id:
            recipe_name = str(request.data.get('recipe_name', ''))
            recipe_ingredients = request.data.get('recipe_ingredients', '')
            recipe_methods = request.data.get('recipe_methods', '')

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

    def get(self, current_user, id):
        """"Method to retrieve all the recipes that belong to a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []
          - TokenParameter: []

        parameters:
            - in: path
              name: id
              required: true
              type: integer

            - in: query
              name: page
              description: The number of pages of the results to be returned

            - in: query
              name: limit
              description: The limit of recipes to be returned by the paginated results

        responses:
          200:
            schema:
              id: recipes
              description: fetching a recipe
        """
        page = request.args.get('page', '')
        limit =request.args.get('limit', '')

        if not page:
            page = 1
        else:
            try:
                page = int(request.args.get('page'))
                if page < 1 and int(page) is True:
                    return {"message": "Page number can only be an integer"}, 400
            except Exception:
                return {"message": "Page number not valid"}

        if not limit:
            limit = 20
        else:
            try:
                limit = int(request.args.get('limit'))
                if limit < 1 and int(limit) is True:
                    return {"message": "Limit can only be an integer"}, 400
            except Exception:
                return {"message": "Limit is not a valid number "}, 400
        
        category_id = id
        recipes = Recipes.get_all_user_recipes(category_id).paginate(page, limit)
        results = []
        for recipe in recipes.items:
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
           

class recipes_manipulation(MethodView):
    """Class to handle GET, PUT and DELETE for individual recipes in a category
    """
    methods = ['GET', 'PUT', 'DELETE']
    decorators = [token_required]
    def get(self, current_user, id, recipe_id):
        """Method to get a specific recipe in a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []
          - TokenParameter: []

        parameters:
            - in: path
              name: id
              required: true
              description: Category id of the category
              type: integer

            - in: path
              name: recipe_id
              required: true
              description: Recipe id
              type: integer
        responses:
          200:
            schema:
              id: recipes
              description: fetching a single recipe
        """
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

    def put(self, current_user, id, recipe_id):
        """Method to edit a recipe in a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []
          - TokenParameter: []

        parameters:
            - in: path
              name: id
              required: true
              description: Category id of the category
              type: integer

            - in: body
              name: recipe_name
              required: true
              description: New Recipe name of the recipe
              type: integer

            - in: path
              name: recipe_id
              required: true
              description: Recipe id
              type: integer
        responses:
          200:
            schema:
              id: recipes
              description: editing a recipe
        """
        regex_pattern = "[a-zA-Z- .]+$"
        category_id = id
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

    def delete(self, current_user, id, recipe_id):
        """Method to delete a recipe in a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []
          - TokenParameter: []

        parameters:
            - in: path
              name: id
              required: true
              description: Category id of the category
              type: integer
            - in: path
              name: recipe_id
              required: true
              description: Recipe id
              type: integer
        responses:
          200:
            description: Successfully deleted a category
        """
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

class recipeSearch(MethodView):
    """Class to search a recipe in a particular category
    """
    methods=['GET']
    decorators=[token_required]
    
    def get(self, current_user, id):
        """Method to search a recipe using a get request
        ---
        tags:
          - Recipes
        produces:
          - application/json
        security:
          - TokenHeader: []
          - TokenParameter: []

        parameters:
            - in: path
              name: id
              description: category id that the recipe belongs to

            - in: query
              name: q
              description: The recipe to be searched for

            - in: query
              name: page
              description: The number of pages of the results to be returned

            - in: query
              name: limit
              description: The limit of recipes to be returned by the paginated results

        responses:
          200:
            schema:
              id: recipes
              description: fetching a single recipe
        """
        q = request.args.get('q', '')
        page = request.args.get('page', '')
        limit =request.args.get('limit', '')

        if not page:
            page = 1
        else:
            try:
                page = int(request.args.get('page'))
                if page < 1 and int(page) is True:
                    return {"message": "Page number can only be an integer"}, 400
            except Exception:
                return {"message": "Page number not valid"}

        if not limit :
            limit = 20
        else:
            try:
                limit = int(request.args.get('limit'))
                if limit < 1 and int(limit) is True:
                    return {"message": "Limit can only be an integer"}, 400
            except Exception:
                return {"message": "Limit is not a valid number "}, 400
        
        if q:
            category_id = id
            recipes = Recipes.query.filter(Recipes.recipe_name.ilike('%' + q + \
            '%')).filter(Recipes.category_id==category_id).paginate(per_page=limit, page=page)
            
            #recipes = Recipes.get_all_user_recipes(category_id).paginate(page, limit)
            results = []
            for recipe in recipes.items:
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
        else:
            response = {'message': 'No search item provided'}
            return make_response(jsonify(response)), 200   
        

recipe_search_view = recipeSearch.as_view('recipe_search_view')
recipe_post_get_view = Recipe.as_view('recipe_post_get_view')
recipe_manipulation_view = recipes_manipulation.as_view('recipe_manipulation_view')

