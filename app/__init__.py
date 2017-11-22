from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def make_app(config_name):
    from app.models import Categories

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/categories/', methods=['POST'])
    def categories_post():
        """"Method to add a new category to the endpoint"""
        print("ok")
        if request.method == "POST":
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
                response = {'message':category_name}
                response = jsonify(response)
                response.status_code = 401
                return response

    @app.route('/categories/', methods=['GET'])
    def categories_get():
        """"Method to get all categories"""
        if request.method == "GET":
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

    @app.route('/categories/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def categories_manipulation(id, **kwargs):
        # retrieve a category using it's ID
        category = Categories.query.filter_by(id=id).first()
        if not category:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            category.delete_categories()
            return {
                       "message": "category{} deleted successfully".format(category.id)
                   }, 200

        elif request.method == 'PUT':
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
        else:
            # GET
            response = jsonify({
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            })
            response.status_code = 200
            return response
    return app