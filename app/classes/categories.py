"""Class to handle category creation, viewing and manipulation
"""
import re
from app.decorators import token_required
from app.models import Categories
from flask import request, jsonify, make_response
from flask.views import MethodView


class Category(MethodView):
    """Class to handle post and get for multiple categories
    """
    methods = ['GET', 'POST']
    decorators = [token_required]

    def post(self, current_user):
        """"Method to add a new category to the endpoint
        ---
        tags:
            - Categories
        produces:
            - application/json
        security:
          - TokenHeader: []

        parameters:
            - in: body
              name: Category Name
              descrption: Name of the category
              required: true
              type: string
              schema:
                id: categories
                properties:
                  category_name:
                    type: string
                    default: Breakfast

        responses:
          200:
            schema:
              id: categories
              properties:
                category_name:
                  type: string
                  default: Breakfast
          400:
            description: category name not valid
          400:
            description: category name not provided
          400:
            description: category name exists
          401:
            description: category not created
          201:
            description: category created
        """
        regex_pattern = "[a-zA-Z- .]+$"
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
            category_details = Categories.query.filter_by(
                category_name=category_name, created_by=current_user.id).first()

            if category_details:
                response = {'message': 'Category name exists'}
                return make_response(jsonify(response)), 400

            category = Categories(
                category_name=category_name, created_by=current_user.id)
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

    def get(self, current_user):
        """"Method to get all categories of a user
        ---
        tags:
            - Categories
        produces:
            - application/json
        security:
          - TokenHeader: []
          - TokenParameter: []
        parameter:
          - in: path
        responses:
          200:
            description: Display all the categories of a user
            schema:
              id: Categories
              properties:
                    category_name:
                     type: json
                     default: breakfast
                    created_by:
                     type: integer
                     default: 2
                    date_created:
                     type: string
                     default: Wed 20 Dec
                    date_modified:
                     type: string
                     default: Wed 20 Dec
                    id:
                     type: integer
                     default: 1
        """
        page = None
        limit = None
        try:
            if not page or page is None or page < 1 or not isinstance(page, int):
                page = 1
            page = int(request.args.get('page', 1))
        except Exception:
            return {"message": "Page number not valid"}, 400

        try:
            if not limit or limit is None or limit < 1 or not isinstance(limit, int):
                limit = 10
            limit = int(request.args.get('limit', 10))
        except Exception:
            return {"message": "Limit is not a valid number "}, 400

        categories = Categories.get_all_user_categories(
            current_user.id).paginate(page, limit)
        results = []
        for category in categories.items:
            category_object = {
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            }
            results.append(category_object)
        if len(results) <= 0:
            response = {'message': 'No  category found '}
            response = make_response(jsonify(response)), 404
            return response
        response = jsonify(results)
        response.status_code = 200

        return response


class CategoriesManipulation(MethodView):
    """Class to handle manipulation of categories using PUT, POST, DELETE and GET
    """
    methods = ['GET', 'PUT', 'DELETE']
    decorators = [token_required]

    def get(self, current_user, id):
        """Method to fetch a single category using its id
        ---
        tags:
            - Categories
        produces:
            - application/json
        summary: fetch a category by id
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the category to retrieve
            type: string
        security:
          - TokenHeader: []
          - TokenParameter: []
        responses:
          200:
            description: Display all the categories of a user
            schema:
              id: Category
              properties:
                    category_name:
                     type: json
                     default: breakfast
                    created_by:
                     type: integer
                     default: 2
                    date_created:
                     type: string
                     default: Wed 20 Dec
                    date_modified:
                     type: string
                     default: Wed 20 Dec
                    id:
                     type: integer
                     default: 1

        """
        category = Categories.query.filter_by(
            id=id, created_by=current_user.id).first()
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

    def put(self, current_user, id):
        """Method to edit a sigle category
        ---
        tags:
            - Categories
        produces:
            - application/json
        summary: fetch a category by id
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the category to retrieve
            type: string
          - in: body
            name: category_name
            required: true
            description: Category name of the category Id to edit
            type: string
            schema:
              id: category
              properties:
                    category_name:
                     type: json
                     default: breakfast
        security:
          - TokenHeader: []
          - TokenParameter: []
        responses:
          200:
            description: Edit a user category
            schema:
              id: Category
              properties:
                    category_name:
                     type: json
                     default: breakfast
                    created_by:
                     type: integer
                     default: 2
                    date_created:
                     type: string
                     default: Wed 20 Dec
                    date_modified:
                     type: string
                     default: Wed 20 Dec
                    id:
                     type: integer
                     default: 1
        """
        regex_pattern = "[a-zA-Z- .]+$"

        category = Categories.query.filter_by(
            id=id, created_by=current_user.id).first()
        category_name = str(request.data.get('category_name', ''))

        if not category_name:
            response = {'message': 'category name not provided'}
            return make_response(jsonify(response)), 400

        if not re.search(regex_pattern, category_name):
            response = {'message': 'Category name is not valid'}
            return make_response(jsonify(response)), 400

        if not category:
            response = {'message': 'Category does not exist'}
            return make_response(jsonify(response)), 404
        else:
            category_name = re.sub(r'\s+', ' ', category_name).strip()
            category_name = None if category_name == " " else category_name.title()
            category_details = Categories.query.filter_by(
                category_name=category_name, created_by=current_user.id).first()

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

    def delete(self, current_user, id):
        """Method to delete a single category using its category id
        ---
        tags:
            - Categories
        produces:
            - application/json
        summary: fetch a category by id
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the category to retrieve
            type: string
        security:
          - TokenHeader: []
          - TokenParameter: []
        responses:
          200:
            description: delete a user category
            schema:
              properties:
                    message:
                     type: json
                     default: category name deleted

        """
        category = Categories.query.filter_by(
            id=id, created_by=current_user.id).first()
        if not category:
            response = {'message': 'Category does not exist'}
            return make_response(jsonify(response)), 404
        else:
            category.delete_categories()
            return {
                "message": "successfully deleted category" .format(category.id)
            }, 200


class CategorySearch(MethodView):
    """Class to search a category using pagination
    """
    methods = ['GET']
    decorators = [token_required]

    def get(self, current_user):
        """method to search categories of a particular user
        ---
        tags:
            - Categories
        produces:
            - application/json
        summary: fetch a category defined in a search
        parameters:
          - in: query
            name: q
            description: Item to be searched
            type: string
          - in: page
            name: page
            description: Number of pages to return after a search
            type: int
            default: 1
          - in: query
            name: limit
            description: Item to be searched
            type: int
            default: 10

        security:
          - TokenHeader: []
          - TokenParameter: []
        responses:
          200:
            description: Search for a particular category
            schema:
              id: Category
              properties:
                    category_name:
                     type: json
                     default: breakfast
                    created_by:
                     type: integer
                     default: 2
                    date_created:
                     type: string
                     default: Wed 20 Dec
                    date_modified:
                     type: string
                     default: Wed 20 Dec
                    id:
                     type: integer
                     default: 1
        """
        search = request.args.get('q', '')
        page = None
        limit = None
        try:
            if not page or page is None or page < 1 or not isinstance(page, int):
                page = 1
            page = int(request.args.get('page', 1))
        except Exception:
            return {"message": "Page number not valid"}, 400

        try:
            if not limit or limit is None or limit < 1 or not isinstance(limit, int):
                limit = 10
            limit = int(request.args.get('limit', 10))
        except Exception:
            return {"message": "Limit is not a valid number "}, 400

        if search:
            categories = Categories.query.filter(Categories.category_name.ilike(
                '%' + search + '%')).filter(Categories.created_by == current_user.id).paginate(
                    per_page=limit, page=page)

            if not categories:
                response = {'message': 'No  category found '}
                response = make_response(jsonify(response)), 200
                return response
            else:
                results = []
                for category in categories.items:
                    category_object = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'created_by': category.created_by,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    }
                    results.append(category_object)
                return make_response(jsonify(results)), 200
        else:
            response = {'message': 'No search item provided'}
            return make_response(jsonify(response)), 200


category_view_search = CategorySearch.as_view('category_view_search')
category_view_post = Category.as_view('category_view_post')
category_manipulation = CategoriesManipulation.as_view('category_manipulation')
