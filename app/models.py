"""Stores all models from the user to categories and recipes
"""
from app import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt
import os
from instance.config import Config


class User(db.Model):
    """The class defines the users table"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    username = db.Column(db.String(256))
    secret_word = db.Column(db.String(256))
    password = db.Column(db.String(256), nullable=False)
    # Delete all the categories that belong to a user if the owner is deleted from the db
    categories = db.relationship(
        'Categories', order_by='Categories.id', cascade="all, delete-orphan")

    def __init__(self, email, password, username, secret_word):
        """
        constructor method to initialize class
        variables, username, password, secret_word and email
        """
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.username = username
        self.secret_word = Bcrypt().generate_password_hash(secret_word).decode()

    def password_check(self, password):
        """
        validates if stored password is the user
         password by comparing the hashed and the provided password
         """
        return Bcrypt().check_password_hash(self.password, password)

    def secret_word_check(self, secret_word):
        """
        validates if stored password is the user
        password by comparing secret_word hashed and the provided secret word
         """
        return Bcrypt().check_password_hash(self.secret_word, secret_word)

    def save(self):
        """
        The method saves a user to the database if all
        conditions are met
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def password_hash(password):
        """method to hash provided password
        """
        password = Bcrypt().generate_password_hash(password).decode()
        return password

    @staticmethod
    def user_token_generator(user_id):
        """" Method to generate a token for user identification """
        app_secret = os.getenv('SECRET', '#%$#%$^FDFGFGdf')
        try:
            # set up a payload with an expiration time
            token_payload = {
                'exp': datetime.utcnow() + timedelta(hours=4),
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
        app_secret = os.getenv('SECRET', '#%$#%$^FDFGFGdf')
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
    recipes = db.relationship(
        'Recipes', order_by='Recipes.id', cascade="all, delete-orphan")

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
    def get_all_user_categories(user_id):
        """
        This method fetches all the recipe categories
        that belong to a user.
        """
        return Categories.query.filter_by(created_by=user_id)

    def delete_categories(self):
        """This method deletes a recipe category belonging to a user"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """method simply tells Python how to print objects of the Category class"""
        return "<Categories: {}>".format(self.category_name)


class Recipes(db.Model):
    """Class to define the recipe categories table layout in the db"""

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

    def __init__(self, recipe_name, recipe_ingredients, recipe_methods, category_id):
        """
        Constructor to initialize the class variables, category
        name and the owner
        """
        self.recipe_name = recipe_name
        self.recipe_ingredients = recipe_ingredients
        self.recipe_methods = recipe_methods
        self.category_id = category_id

    def save(self):
        """
        method to save a category name both on update and creation
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_user_recipes(category_id):
        """
        This method fetches all the recipe categories
        that belong to a user.
        """
        return Recipes.query.filter_by(category_id=category_id)

    def delete_recipes(self):
        """ This method deletes a recipe category belonging to a user """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """method simply tells Python how to print objects of the Category class"""
        return "<Recipes: {}>".format(self.recipe_name)


class Sessions(db.Model):
    """Class to store user login sessions
    """
    __tablename__ = 'token_blacklist'
    id = db.Column(db.Integer, primary_key=True)
    auth_token = db.Column(db.String(256), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, auth_token):
        """Constructor method for sesions class
        """
        self.auth_token = auth_token

    def check_logout_status(self, auth_token):
        """Method to check if a user is logged out
        """
        logout_state = Sessions.query.filter_by(auth_token=auth_token).first()
        if logout_state:
            return True
        else:
            return False

    def save(self):
        """Method to save the sessions or to update the db sessions
        """
        db.session.add(self)
        db.session.commit()
