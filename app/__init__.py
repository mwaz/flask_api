from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy


# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def make_app(config_name):
    from app.models import Categories
    from app.classes import categories

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.classes.categories import category_view_post,category_manipulation
    app.add_url_rule('/yummy_api/v1/categories/', view_func=category_view_post)
    app.add_url_rule('/yummy_api/v1/categories/<int:id>', view_func=category_manipulation)

    from app.classes.recipes import recipe_post_get_view, recipe_manipulation_view
    app.add_url_rule('/yummy_api/v1/categories/<int:id>/recipes/', view_func=recipe_post_get_view)
    app.add_url_rule('/yummy_api/v1/categories/<int:id>/recipes/<int:recipe_id>', view_func=recipe_manipulation_view)

    from app.auth.authentication import user_registration_view,user_login_view
    app.add_url_rule('/yummy_api/v1/auth/register', view_func=user_registration_view, methods=['POST'])
    app.add_url_rule('/yummy_api/v1/auth/login', view_func=user_login_view, methods=['POST'])

    return app