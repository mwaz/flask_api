from marshmallow import ValidationError
import re


def recipe_validation(recipe, *argv):
    error = None
    regex_pattern = "[a-zA-Z0-9-]+$"

    if recipe:
        recipe = re.sub(r'\s+', '', recipe).strip()
    recipe = None if recipe == "  " else recipe.title()

    if not re.search(regex_pattern, recipe):
        error = ValidationError('recipe name cannot be empty or with invalid characters')

    for arg in argv:
        if arg:
            arg = re.sub(r'\s+', '', arg).strip()
        arg = None if arg == "  " else arg

        if not arg:
            error = ValidationError('Kindly provide ingredients and methods')

        if error:
            raise error

