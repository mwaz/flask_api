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
    app.add_url_rule('/flask_api/v1/categories/', view_func=category_view_post)
    app.add_url_rule('/flask_api/v1/categories/<int:id>', view_func=category_manipulation)
    return app