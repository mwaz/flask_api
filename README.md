[![Coverage Status](https://coveralls.io/repos/github/mwaz/flask_api/badge.svg?branch=develop)](https://coveralls.io/github/mwaz/flask_api?branch=develop)[![Build Status](https://travis-ci.org/mwaz/flask_api.svg?branch=develop)](https://travis-ci.org/mwaz/flask_api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6fb4d5ea061346429bfdb9a9ac62f55c)](https://www.codacy.com/app/mwaz/flask_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mwaz/flask_api&amp;utm_campaign=Badge_Grade)

# Yummy Recipes Application API
Challenge 3: A Flask API that enables one to create a recipe category, add, delete and update a category
API also allows one to create recipes, update delete them using API endpoints


Find Heroku App [here][] 

[here]: https://yummy-recipies-api.herokuapp.com/

# Requirements

* python 3 
* Postgres Database Engine


# Installation

1 Clone the Github Repositorty'

use ssh

   ```
   $ git clone https://github.com/mwaz/flask_api.git
   ```
      
2 Install the Database Engine and Pip

  ```
  $ sudo apt-get install python3-pip python3-dev libpq-dev
  ```


4 Create the PostgreSQL Database and User

```
   $ sudo -u postgres psql
   $ sudo -u postgres createuser postgres
   $ sudo -u postgres createdb flask_api
   
   postgres=# GRANT ALL PRIVILEGES ON DATABASE flask_api TO postgres;
```

5 Create  and run database migrations

```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

6 Set Up and activate a virtual environment
```
$ virtualenv venv
$ source venv/bin/activate
```

7 Install all application requirements using requirements.txt

```
  $ pip install -r requirements.txt
```

8 Run the Application

```
$ python run.py
```
Interact with the API :-), send http requests using Postman


# Screenshot

![image](https://user-images.githubusercontent.com/10160787/34572706-1a33447e-f183-11e7-822e-550658989ad1.png)


## User API Endpoints

URL Endpoint	|               HTTP requests   | access| status|
----------------|-----------------|-------------|------------------
/flask_api/v1/auth/register   |      POST	| Register a new user|publc
/flask_api/v1/auth/login	  |     POST	| Login and retrieve token|public

## Categories  API Endpoints

URL Endpoint	|               HTTP requests   | access| status|
----------------|-----------------|-------------|------------------
/flask_api/v1/categories/	              |      POST	|  Create a new recipe category|private
/flask_api/v1/categories/	              |      GET	|  Retrieve all categories  for user|private
/flask_api/v1/categories/search/?q=&limit&page	              |      GET	|  Retrieve all categories for a given search |private
/flask_api/v1/categories/<category_id>/   |  	 GET	   | Retrieve a category by ID | private
/flask_api/v1/categories/<category_id>/	  |      PUT	|     Update a category |private
/flask_api/v1/categories/<category_id>/   |      DELETE	| Delete a category |private

## Recipes  API Endpoints

URL Endpoint	|               HTTP requests   | access| status|
----------------|-----------------|-------------|------------------
/flask_api/v1/categories/<category_id>/recipes/  |  GET  |Retrive recipes in a given category |private
/flask_api/v1/categories/<category_id>/recipes/     |     POST	| Create recipes in a category|private
/flask_api/v1/categories/<category_id>/recipes/search/?q=&limit&page  |      GET	| Retrieve all recipes for a given search |private
/flask_api/v1/categories/<category_id>/recipes/<recipe_id>/|	DELETE	| Delete a recipe in a category  |private
/flask_api/v1/categories/<category_id>/recipes/<recipe_id>/ |	PUT   	|update recipe details |private

Run the APIs on postman to ensure they are fully functioning.

