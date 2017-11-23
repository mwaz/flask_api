from app.models import Categories
from flask import request, jsonify, abort
from flask.views import MethodView



class Category(MethodView):
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    # @app.route('/flask_api/v1/categories/', methods=['POST'])
    def post(self):
        """"Method to add a new category to the endpoint"""
        category_name = str(request.data.get('category_name', ''))
        if category_name:
            category = Categories(category_name=category_name)
            category.save()
            response = jsonify({
                'id': category.id,
                'category_name': category.category_name,
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

    # @app.route('/flask_api/v1/categories/', methods=['GET'])
    def get(self):
        """"Method to get all categories"""
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

    # @app.route('/flask_api/v1/categories/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def categories_manipulation(id, **kwargs):
        # retrieve a category using it's ID
        category = Categories.query.filter_by(id=id).first()
        if not category:
            # Raise an HTTPException with a 404 not found status code
            abort(404)




class CategoriesManipulation(MethodView):
    methods = ['GET','POST', 'PUT', 'DELETE']
    def get(self, id):
        category = Categories.query.filter_by(id=id).first()
        response = jsonify({
            'id': category.id,
            'category_name': category.category_name,
            'date_created': category.date_created,
            'date_modified': category.date_modified
        })
        response.status_code = 200
        return response
    def put(self, id):
        category = Categories.query.filter_by(id=id).first()
        if not category:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        else:
            category_name = str(request.data.get('category_name', ''))
            category.category_name = category_name
            category.save()
            response = jsonify({
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            })
            response.status_code = 200
            return response
    def delete(self, id):
        category = Categories.query.filter_by(id=id).first()
        if not category:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        else:
           category.delete_categories()
           return {
                    "message": "successfully deleted category".format(category.id)
                  }, 200


category_view_post = Category.as_view('category_view_post')

category_manipulation = CategoriesManipulation.as_view('category_manipulation')