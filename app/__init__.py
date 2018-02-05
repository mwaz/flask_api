from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask import make_response, jsonify, abort


# local import
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
base_url = '/yummy_api/v1'


def make_app(config_name):
    from app.models import Categories
    from app.classes import categories

    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.config['SWAGGER'] = {"swagger": "2.0",
                             "title": "Yummy Recipes",
                             "info": {
                                 "title": "Yummy Recipes API documentation",
                                 "description": "Yummy Recipes provides a way to create recipes and their categories"
                                                " and to manipulate them ",
                                 "version": "1.0.0",
                                 "basepath": '/',
                                 "uiversion": 3,
                             },
                             "securityDefinitions": {
                                 "TokenHeader": {
                                     "type": "apiKey",
                                     "name": "Authorization",
                                     "in": "header"
                                 },
                                
                             },
                             "consumes": [
                                 "application/json",
                             ],
                             "produces": [
                                 "application/json",
                             ],}
                             
    Swagger(app)
    from app.classes.categories import category_view_post, category_manipulation, category_view_search
    app.add_url_rule(base_url + '/categories/', view_func=category_view_post)
    app.add_url_rule(base_url + '/categories/<int:id>',
                     view_func=category_manipulation)
    app.add_url_rule(base_url + '/categories/search/',
                     view_func=category_view_search)

    from app.classes.recipes import recipe_post_get_view, recipe_manipulation_view, recipe_search_view
    app.add_url_rule(base_url + '/categories/<int:id>/recipes/',
                     view_func=recipe_post_get_view)
    app.add_url_rule(base_url + '/categories/<int:id>/recipes/<int:recipe_id>',
                     view_func=recipe_manipulation_view)
    app.add_url_rule(
        base_url + '/recipes/search/', view_func=recipe_search_view)

    from app.auth.authentication import user_registration_view, user_login_view, user_password_reset_view, user_logout_view, send_email_token_view
    app.add_url_rule(base_url + '/auth/register',
                     view_func=user_registration_view, methods=['POST'])
    app.add_url_rule(base_url + '/auth/login',
                     view_func=user_login_view, methods=['POST'])
    app.add_url_rule(base_url + '/auth/password-reset',
                     view_func=user_password_reset_view, )
    app.add_url_rule(base_url + '/auth/password-reset-email',
                     view_func=send_email_token_view, )
    app.add_url_rule(base_url + '/auth/logout', view_func=user_logout_view)

    @app.errorhandler(404)
    def not_found(error):
        """handles error when users enters inappropriate endpoint
        """
        response = {
            'message': 'Page not found'
        }
        return make_response(jsonify(response)), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """ handles errors if users uses method that is not allowed in an endpoint
        """
        response = {
            'message': 'Method not allowed'
        }
        return make_response(jsonify(response)), 405

    return app

