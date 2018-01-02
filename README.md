[![Coverage Status](https://coveralls.io/repos/github/mwaz/flask_api/badge.svg?branch=develop)](https://coveralls.io/github/mwaz/flask_api?branch=develop)[![Build Status](https://travis-ci.org/mwaz/flask_api.svg?branch=develop)](https://travis-ci.org/mwaz/flask_api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6fb4d5ea061346429bfdb9a9ac62f55c)](https://www.codacy.com/app/mwaz/flask_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mwaz/flask_api&amp;utm_campaign=Badge_Grade)

# Yummy Recipes Application API
Challenge 3: A Flask API that enables one to create a recipe category, add, delete and update a category
API also allows one to create recipes, update delete them using API endpoints

# Installation and Setup

Clone the repo

git clone https://github.com/mwaz/flask_api.git

use ssh

    git@github.com:mwaz/flask_api.git

go to the root folder

cd flask_api

Create the virtual environment

$virtualenv venv

Activate the virtual environment

$source venv/bin/activate

# Install the requirements

$pip install -r requirements.txt

Set Up Environment


# Run Database Migrations

 Initialize, migrate, upgrade the database

$python manage.py db init

$python manage.py db migrate

$python manage.py db upgrade

Launch the Progam

# Run

$python run.py

Interact with the API, send http requests using Postman

# API Endpoints

URL Endpoint	|               HTTP requests   | access| status|
----------------|-----------------|-------------|------------------
/flask_api/v1/auth/register/   |      POST	| Register a new user|publc
/flask_api/v1/auth/login/	  |     POST	| Login and retrieve token|public
/flask_api/v1/categories/	              |      POST	|  Create a new recipe category|private
/flask_api/v1/categories	              |      GET	|  Retrieve all categories  for user|private
/flask_api/v1/categories/<category_id>/   |  	 GET	   | Retrieve a category by ID | private
/flask_api/v1/categories/<category_id>/	  |      PUT	|     Update a category |private
/flask_api/v1/categories/<category_id>/   |      DELETE	| Delete a category |private
/flask_api/v1/categories/<category_id>/recipes/  |  GET  |Retrive recipes in a given category |private
/flask_api/v1/categories/<category_id>/recipes/     |     POST	| Create recipes in a category|private
/flask_api/v1/categories/<category_id>/recipes/<recipe_id>/|	DELETE	| Delete a recipe in a category  |prvate
/flask_api/v1/categories/<category_id>/recipes/<recipe_id>/ |	PUT   	|update recipe details |private

Run the APIs on postman to ensure they are fully functioning.

