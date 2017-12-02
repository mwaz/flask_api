from app import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt
import os
from instance.config import Config
class User(db.Model):
    """The class defines the users table"""

    __tablename__ = 'users'

    """
    Table columns:
    id - defines the unique key to identify a particular user in the users table
    email - defines email field of a user
    password - defines the password belonging to a user 
    """
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), nullable=False, unique=True)

    password = db.Column(db.String(256), nullable=False)

    # Delete all the categories that belong to a user if the owner is deleted from the db
    categories = db.relationship(
        'Categories', order_by='Categories.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """
        constructor method to initialize class 
        variables, username and email
        """
        self.email = email
        # generates password hash using 'BYCRYPT'
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_check(self, password):
        """
        validates if stored password is the user
         password by comparing the hashed and the provided password
         """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """ 
        The method saves a user to the database if all 
        conditions are met
        """
        db.session.add(self)
        db.session.commit()

    def user_token_generator(self, user_id):
        """" Method to generate a token for user identification """
        app_secret = os.getenv('SECRET')
        try:
            # set up a payload with an expiration time
            token_payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'usr': user_id
            }
            # byte string token created with the payload and the SECRET key
            jwt_string = jwt.encode(
                token_payload,
                app_secret,
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)


    @staticmethod
    def decode_token(token):
        """Method to decode the provided token"""
        app_secret = os.getenv('SECRET')
        try:
            payload = jwt.decode(token, app_secret)
            return payload['usr']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

class Categories(db.Model):
    """ Class to define the recipe categories table layout in the db """

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)  # primary key
    category_name = db.Column(db.String(256), nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, category_name, created_by):
        """
        Constructor to initialize the class variables, category
        name and the owner
        """
        self.category_name = category_name
        self.created_by = created_by

    def save(self):
        """
        method to save a category name both on update and creation
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_user_categories():
        """
        This method fetches all the recipe categories
        that belong to a user.
        """
        return Categories.query.filter_by()

    def delete_categories(self):
        """ This method deletes a recipe category belonging to a user """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """method simply tells Python how to print objects of the Category class"""
        return "<Categories: {}>".format(self.category_name)


class Recipes(db.Model):
    """ Class to define the recipe categories table layout in the db """

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)  # primary key
    recipe_name = db.Column(db.String(256), nullable=False)
    recipe_ingredients = db.Column(db.String(256), nullable=False)
    recipe_methods = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.id))

    def __init__(self, recipe_name, recipe_ingredients,recipe_methods, category_id):
        """
        Constructor to initialize the class variables, category
        name and the owner
        """
        self.recipe_name = recipe_name
        self.recipe_ingredients = recipe_ingredients
        self.recipe_methods = recipe_methods
        self.category_id= category_id

    def save(self):
        """
        method to save a category name both on update and creation
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_user_recipes(userid):
        """
        This method fetches all the recipe categories
        that belong to a user.
        """
        return Recipes.query.filter_by(created_by=userid)

    def delete_recipes(self):
        """ This method deletes a recipe category belonging to a user """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """method simply tells Python how to print objects of the Category class"""
        return "<Recipes: {}>".format(self.recipe_name)
