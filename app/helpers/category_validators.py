"""Methods to validate a users category
"""
from marshmallow import ValidationError
import re


def category_validation(category_name):
    """Validation method for creating a category
    """
    error = None
    regex_pattern = "[a-zA-Z0-9- .]+$"

    if category_name:
        category_name = re.sub(r'\s+', ' ', category_name).strip()
    category_name = None if category_name == " " else category_name

    if not category_name:
        error = ValidationError('category name not valid')

    if not re.findall(regex_pattern, category_name):
        error = ValidationError('Category name is not valid')

    if error:
        raise error
