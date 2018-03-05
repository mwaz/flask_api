"""Class to handle category creation, viewing and manipulation
"""
from app.helpers.decorators import token_required
from app.models import Categories
from flask import request, jsonify, make_response
from flask.views import MethodView
from app.helpers.category_validators import category_validation


class Category(MethodView):
    """Class to handle post and get for multiple categories
    """
    methods = ['GET', 'POST']
    decorators = [token_required]

    def post(self, current_user):
        """Method to add a new category to the endpoint
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
                id: categories create
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
          400:
            description: category name not valid
          400:
            description: category name not provided
          400:
            description: category name exists
          401:
            description: category not created because user is unauthenticated
          201:
            description: category created
        """

        try:
            category_name = str(request.data.get('category_name', ''))
            category_details = Categories.query.filter_by(
                    category_name=category_name.title(), created_by=current_user.id).first()
            category_validation(category_name)
            if category_details:
                response = {'message': 'Category name exists'}
                return make_response(jsonify(response)), 400

            category = Categories(
                category_name=category_name.title(), created_by=current_user.id)
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
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400

    def get(self, current_user):
        """Method to get all categories of a user in a paginated way
        ---
        tags:
            - Categories
        produces:
            - application/json
        security:
            - TokenHeader []
        parameters:
            - in: query
              name: page
              description: The number of pages of the results to be returned

            - in: query
              name: limit
              description: The limit of recipes to be returned by the paginated results


        responses:
          200:
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

          400:
            description: Limit number not valid
          400:
            description: Limit number not valid
          400:
            description: Page number not valid
          404:
            description: No category found
        """

        page = request.args.get('page', default=1, type=int)

        limit = request.args.get('limit', default=9, type=int)

        categories = Categories.get_all_user_categories(
            current_user.id).paginate(page, limit, error_out=False)
        results = []
        for category in categories.items:

            category_object = {
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'date_modified': category.date_modified,
                'previous_page': categories.prev_num,
                'next_Page': categories.next_num

            }

            results.append(category_object)
        if len(results) <= 0:
            response = {'message': 'No  category found '}
            response = make_response(jsonify(response)), 404
            return response
        response = jsonify(results)
        response.status_code = 200

        return response


class ManipulateCategory(MethodView):
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
          404:
            description: No category found
          200:
            description: OK

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
          400:
            description: Bad Requests on category edit route
          404:
            description: Category does not exist
          200:
            description: OK
        """

        try:
            category = Categories.query.filter_by(
                id=id, created_by=current_user.id).first()
            category_name = str(request.data.get('category_name', ''))
            category_validation(category_name)

            if not category:
                response = {'message': 'Category does not exist'}
                return make_response(jsonify(response)), 404

            category_details = Categories.query.filter_by(
                category_name=category_name, created_by=current_user.id).first()

            if category_details:
                response = {'message': 'Category name exists',
                            'status': 'fail'}
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
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 400

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
        responses:
          200:
            description: delete a user category
            schema:
              properties:
                    message:
                     type: json
                     default: category name deleted
          404:
            description: Category does not exist
          200:
            description: Category Deleted
        """
        category = Categories.query.filter_by(
            id=id, created_by=current_user.id).first()
        if not category:
            response = {'message': 'Category does not exist',
                        'status': 'error'}
            return make_response(jsonify(response)), 404
        else:
            category.delete_categories()
            response = {'message': 'successfully deleted category',
                        'status': 'success',
                        'id': '{}'.format(category.id)}
            return make_response(jsonify(response)), 200


class SearchCategory(MethodView):
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
          400:
            description: Bad Requests on search route
          200:
            description: OK
        """

        search = request.args.get('q', '')
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=9, type=int)

        if search:
            categories = Categories.query.filter(Categories.category_name.ilike(
                '%' + search + '%')).filter(Categories.created_by == current_user.id).paginate(
                   page, limit, error_out=False)

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
                        'date_modified': category.date_modified,
                        'previous_page': categories.prev_num,
                        'next_Page': categories.next_num
                    }
                    results.append(category_object)
                if len(results) <= 0:
                    response = {'message': 'No  category found '}
                    response = make_response(jsonify(response)), 404
                    return response
                return make_response(jsonify(results)), 200
        else:
            response = {'message': 'No search item provided',
                        'status': 'error'}
            return make_response(jsonify(response)), 200


category_view_search = SearchCategory.as_view('category_view_search')
category_view_post = Category.as_view('category_view_post')
category_manipulation = ManipulateCategory.as_view('category_manipulation')
