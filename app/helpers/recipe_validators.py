from marshmallow import  ValidationError
import re


def recipe_validation(recipe_name, recipe_methods, recipe_ingredients):
    error = None
    regex_pattern = "[a-zA-Z0-9-]+$"

    if recipe_name:
        recipe_name = re.sub(r'\s+', ' ', recipe_name).strip()
    recipe_name = None if recipe_name == "  " else recipe_name.title()

    if recipe_ingredients:
        recipe_ingredients = re.sub(r'\s+', ' ', recipe_ingredients).strip()
    recipe_ingredients = None if recipe_ingredients == "  " else recipe_ingredients

    if recipe_methods:
        recipe_methods = re.sub(r'\s+', ' ', recipe_methods).strip()
    recipe_methods = None if recipe_methods == "  " else recipe_methods

    if not recipe_name:
        error = ValidationError('Recipe name not provided')

    if not recipe_ingredients:
        error = ValidationError('Recipe ingredients not provided')

    if not recipe_methods:
            error = ValidationError('Recipe preparation methods not provided')

    if not re.search(regex_pattern, recipe_name):
        error = ValidationError('Recipe name is not valid')

    if error:
        raise error
