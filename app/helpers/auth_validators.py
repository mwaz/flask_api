"""Class to validate user input
"""
from marshmallow import Schema, fields, ValidationError
from validate_email import validate_email
import re


def user_registration_validation(email, username, password, secret):
    """
    Method to check if email data is valid
    """
    error = None
    email = None if email == " " else email.lower()
    valid_email = validate_email(email)

    if username:
        username = re.sub(r'\s+', ' ', username).strip()
    username = None if username == " " else username.title()

    if not email or not password or not username:
        error = ValidationError('Kindly provide all details')
    if not len(password) >= 6:
        error = ValidationError('Password should be more than six characters')
    if not secret:
        error = ValidationError('Kindly provide a SECRET word')
    if not username:
        error = ValidationError('{} is not a valid username'.format(username))
    if not valid_email:
        error = ValidationError('{} is not a valid email'.format(email))

    if error:
        raise error


def user_login_validation(email, password):
    """
    Method to  validate login credentials of a user
    """
    error = None
    if not email or not password:
        error = ValidationError('Kindly Provide email and Password')

    if error:
        raise error


def password_reset_validation(email, reset_password, secret):
    """Validators to check password Reset
    """
    error = None
    if reset_password:
        reset_password = re.sub(r'\s+', ' ', reset_password).strip()
    reset_password = None if reset_password == " " else reset_password

    if not reset_password:
        error = ValidationError('Kindly provide a reset Password')

    if not email:
        error = ValidationError('Invalid user email')

    if not secret:
        error = ValidationError('Invalid Secret Word')

    if error:
        raise error





