"""Class to handle creation  and manipulation of recipe categories
"""

import re
from app.helpers.decorators import token_required
from app.models import Recipes
from flask import request, jsonify, make_response
from flask.views import MethodView
from app.helpers.recipe_validators import recipe_validation


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
          400:
            description: Bad Request on recipe creation route
          201:
            description: Success in creating a recipe
          404:
            description: Category does not exist
        """
        category_id = id
        if category_id:
            try:
                recipe_name = str(request.data.get('recipe_name', ''))
                recipe_ingredients = request.data.get('recipe_ingredients', '')
                recipe_methods = request.data.get('recipe_methods', '')

                recipe_validation(recipe_name, recipe_methods, recipe_ingredients)
                recipe = Recipes(recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                                 recipe_methods=recipe_methods, category_id=category_id)
                recipe_details = Recipes.query.filter_by(
                    category_id=category_id, recipe_name=recipe_name).first()

                if recipe_details:
                    response = {'message': 'Recipe name exists'}
                    return make_response(jsonify(response)), 400
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

            except Exception:
                response = {'message': 'Category does not exist'}
                return make_response(jsonify(response)), 404

    def get(self, current_user, id):
        """"Method to retrieve all the recipes that belong to a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []
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
          400:
            description: Page Number or limit is not valid
          200:
            description: OK
        """

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        category_id = id
        recipes = Recipes.get_all_user_recipes(
            category_id).paginate(page, limit, error_out=False)
        results = []
        for recipe in recipes.items:
            recipe_obj = {'id': recipe.id,
                          'recipe_name': recipe.recipe_name,
                          'recipe_ingredients': recipe.recipe_ingredients,
                          'recipe_methods': recipe.recipe_methods,
                          'category_id': recipe.category_id,
                          'date_created': recipe.date_created,
                          'date_modified': recipe.date_modified,
                          'previous_page': recipes.prev_num,
                          'next_Page': recipes.next_num

                         }

            results.append(recipe_obj)
        if len(results) <= 0:
            response = {'message': 'No  recipe found '}
            response = make_response(jsonify(response)), 404
            return response
        response = jsonify(results)
        response.status_code = 200
        return response


class ManipulateRecipes(MethodView):
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
          404:
            description: No recipe Found
          200:
            description: OK
        """
        recipe = Recipes.query.filter_by(category_id=id, id=recipe_id).first()
        if not recipe:
            response = {'message': 'No recipe found'}
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
          400:
            description: Recipe Name, Ingredients or methods not provided or valid
          404:
            description: No recipe found
          201:
            description: Successfully edited a recipe
        """
        try:
            category_id = id
            recipe = Recipes.query.filter_by(
                category_id=category_id, id=recipe_id).first()
            recipe_name = str(request.data.get('recipe_name', ''))
            recipe_ingredients = str(request.data.get('recipe_ingredients', ''))
            recipe_methods = str(request.data.get('recipe_methods', ''))
            recipe_validation(recipe_name,recipe_methods, recipe_ingredients)

            if not recipe:
                response = {'message': 'No recipe found'}
                response = make_response(jsonify(response)), 404
                return response
            else:
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
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400

    def delete(self, current_user, id, recipe_id):
        """Method to delete a recipe in a category
        ---
        tags:
            - Recipes
        produces:
            - application/json
        security:
          - TokenHeader: []
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
          404:
            description: No recipe found
          200:
            description: OK
        """
        recipe = Recipes.query.filter_by(category_id=id, id=recipe_id).first()
        if not recipe:
            response = {'message': 'No recipe found'}
            response = make_response(jsonify(response)), 404
            return response
        else:
            recipe.delete_recipes()
            response = {
                "message": "successfully deleted category".format(recipe.id)}
            response = make_response(jsonify(response)), 200
            return response


class SearchRecipe(MethodView):
    """Class to search a recipe in a particular category
    """
    methods = ['GET']
    decorators = [token_required]

    def get(self, current_user, id):
        """Method to search a recipe using a get request
        ---
        tags:
          - Recipes
        produces:
          - application/json
        security:
          - TokenHeader: []


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
          400:
            description: Page or page limit is not valid
          200:
            description: OK
        """
        search = request.args.get('q', '')
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        if search:
            category_id = id
            recipes = Recipes.query.filter(Recipes.recipe_name.ilike(
                '%' + search + '%')).filter(Recipes.category_id == category_id).paginate(
                    per_page=limit, page=page, error_out=False)
            results = []
            for recipe in recipes.items:
                recipe_obj = {'id': recipe.id,
                              'recipe_name': recipe.recipe_name,
                              'recipe_ingredients': recipe.recipe_ingredients,
                              'recipe_methods': recipe.recipe_methods,
                              'category_id': recipe.category_id,
                              'date_created': recipe.date_created,
                              'date_modified': recipe.date_modified,
                              'previous_page': recipes.prev_num,
                              'next_Page': recipes.next_num
                             }

                results.append(recipe_obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            response = {'message': 'No search item provided'}
            return make_response(jsonify(response)), 200


recipe_search_view = SearchRecipe.as_view('recipe_search_view')
recipe_post_get_view = Recipe.as_view('recipe_post_get_view')
recipe_manipulation_view = ManipulateRecipes.as_view(
    'recipe_manipulation_view')
