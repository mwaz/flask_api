from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import requests, jsonify, abort

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

@app.route('/categories/', methods=[POST, GET])
def categories():
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
            #If not a POST, then its a GET which fetches either one or all categories
            categories = Categories.get_all()
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
    return app