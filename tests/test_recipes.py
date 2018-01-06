"""Base Class to test recipe.py class
"""
import json
import unittest
from app import make_app, db

base_url = 'yummy_api/v1'


class RecipesTestCase(unittest.TestCase):
    """Class to test, creation, deletion and editing recipes
    """

    def setUp(self):
        """method to define varibles to be used in the tests
        """
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.recipes = {'recipe_name': 'New_Recipes',
                        'recipe_ingredients': 'milk',
                        'recipe_methods': 'boil to heat'}

        self.other_recipes = {'recipe_name': 'Another_New_Recipes',
                              'recipe_ingredients': 'Water, Milk',
                              'recipe_methods': 'Heat till Warm'}

        self.categories = {'category_name': 'New_Category'}

        #binds app to the current context
        with self.app.app_context():
            #creates all the tables
            db.create_all()

        #register a user
        user_details = json.dumps(dict({
            "email": "test@test.com",
            "password": "password",
            "username": "User",
            "secret_word": "TOP SECRET"
        }))
        self.client().post(base_url + '/auth/register', data=user_details,
                           content_type="application/json")

        # Login  a test user
        login_details = json.dumps(dict({
            "email": "test@test.com",
            "password": "password"
        }))

        self.login_data = self.client().post(base_url + '/auth/login', data=login_details,
                                             content_type="application/json")

        # login a user and obtain the token
        self.access_token = json.loads(
            self.login_data.data.decode())['access_token']

        # create a category
        self.client().post(base_url + '/categories/',
                                             headers=dict(
                                                 Authorization=self.access_token),
                                             data=self.categories)

    def test_to_create_recipe(self):
        """test method to create a recipe
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "New_Recipe",
                                                 "recipe_ingredients": "milk",
                                                 "recipe_methods": "heat to boil"})
        self.assertEqual(create_recipe.status_code, 201)

        get_created_recipe = self.client().get(base_url + '/categories/1/recipes/',
                                               headers=dict(Authorization=self.access_token))
        self.assertIn('New_Recipe', str(get_created_recipe.data))

    def test_null_recipe_name(self):
        """test if recipe name is null
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": " ",
                                                 "recipe_ingredients": "milk",
                                                 "recipe_methods": "heat to boil"})
        self.assertEqual(create_recipe.status_code, 400)
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'], 'Recipe name is not valid')

    def test_null_recipe_methods(self):
        """test if recipe methods are null
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "New Recipe",
                                                 "recipe_ingredients": "milk",
                                                 "recipe_methods": " "})

        self.assertEqual(create_recipe.status_code, 400)
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'],
                      'Recipe preparation methods not provided')

    def test_null_recipe_ingredients(self):
        """test if recipe ingredients are null
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "New Recipe",
                                                 "recipe_ingredients": "",
                                                 "recipe_methods": "heat to boil"})

        self.assertEqual(create_recipe.status_code, 400)
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'],
                      'Recipe ingredients not provided')

    def test_invalid_recipe_name(self):
        """test if recipe name is valid
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "",
                                                 "recipe_ingredients": "milk, water",
                                                 "recipe_methods": "heat to boil"})
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'], 'Recipe name is not valid')
        self.assertEqual(create_recipe.status_code, 400)

    def test_duplicate_recipe(self):
        """test if recipe is duplicated
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={'recipe_name': 'New_Recipes',
                                                 'recipe_ingredients': 'milk',
                                                 'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 201)
        create_another_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                                   headers=dict(Authorization=self.access_token),
                                                   data=self.recipes)

        self.assertEqual(create_another_recipe.status_code, 400)
        recipe_data = json.loads(create_another_recipe.data.decode())
        self.assertIn(recipe_data['message'], 'Recipe name exists')

    def test_non_existent_category(self):
        """test if category does not exist
        """
        create_recipe = self.client().post(base_url + '/categories/100/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={'recipe_name': 'New_Recipes',
                                                 'recipe_ingredients': 'milk',
                                                 'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 404)
        recipe_details = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_details['message'], 'Category does not exist')

    def test_to_get_all_recipes(self):
        """Test method to get all recipes
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)
        create_another_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                                   headers=dict(Authorization=self.access_token),
                                                   data=self.other_recipes)
        self.assertEqual(create_another_recipe.status_code, 201)

        get_created_recipe = self.client().get(base_url + '/categories/1/recipes/?page=1&limit=1',
                                               headers=dict(Authorization=self.access_token))
        self.assertEqual(get_created_recipe.status_code, 200)

    def test_to_edit_a_recipe_name(self):
        """Test to edit a recipe name
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'edited_recipe_name',
                                              'recipe_ingredients': 'milk, milk',
                                              'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_edit_recipe_with_null_name(self):
        """Test to edit a recipe name with a null name
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': '',
                                              'recipe_ingredients': 'milk, milk',
                                              'recipe_methods': 'boil to heat'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'], 'Recipe name is not valid')

    def test_to_edit_recipe_with_null_recipe_methods(self):
        """Test to edit a recipe name with null recipe methods
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipes',
                                              'recipe_ingredients': 'milk, milk',
                                              'recipe_methods': ''})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'],
                      'Recipe preparation methods not provided')

    def test_to_edit_recipe_with_null_recipe_ingredients(self):
        """Test to edit a recipe name with null recipe ingredients
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipes',
                                              'recipe_ingredients': '',
                                              'recipe_methods': 'heat to boil'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'],
                      'Recipe ingredients not provided')

    def test_edit_invalid_recipe_name(self):
        """Test to edit a recipe name with invalid recipe name
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': '@@@@##$',
                                              'recipe_ingredients': 'ingredients here',
                                              'recipe_methods': 'heat to boil'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'], 'Recipe name is not valid')

    def test_edit_recipe_with_no_recipe_id(self):
        """Test to edit a recipe name with invalid recipe name
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/2',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'new recipe name',
                                              'recipe_ingredients': 'ingredients here',
                                              'recipe_methods': 'heat to boil'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 404)
        self.assertIn(category_data['message'], 'No recipe found')

    def test_to_edit_recipe_ingredients(self):
        """Test to check the edit_recipe_ingredients functionality
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipe_name',
                                              'recipe_ingredients': 'Butter',
                                              'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_edit_recipe_preparation(self):
        """Test to check the edit recipe preparation method functionality
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipe_name',
                                              'recipe_ingredients': 'Butter',
                                              'recipe_methods': 'warm till ready'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_get_recipe_by_id(self):
        """Test to get a single recipe using the recipe id
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        get_recipe = self.client().get(base_url + '/categories/1/recipes/1',
                                       headers=dict(Authorization=self.access_token))
        self.assertIn('New_Recipes', str(get_recipe.data))

    def test_to_check_invalid_recipe_id(self):
        """Test to check if the recipe id supplied is invalid
        """
        get_recipe = self.client().get(base_url + '/categories/1/recipes/2',
                                       headers=dict(Authorization=self.access_token))
        recipe_data = json.loads(get_recipe.data.decode())
        self.assertEqual(get_recipe.status_code, 404)
        self.assertIn(recipe_data['message'], 'No recipe found')

    def test_recipe_delete_by_id(self):
        """Method to test recipe delete by id
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        delete_result = self.client().delete(base_url + '/categories/1/recipes/1',
                                             headers=dict(Authorization=self.access_token))
        self.assertEqual(delete_result.status_code, 200)

    def test_recipe_double_delete(self):
        """Method to test inexistent recipe delete by id
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        delete_result = self.client().delete(base_url + '/categories/1/recipes/1',
                                             headers=dict(Authorization=self.access_token))
        self.assertEqual(delete_result.status_code, 200)

        delete_result = self.client().delete(base_url + '/categories/1/recipes/1',
                                             headers=dict(Authorization=self.access_token))
        self.assertEqual(delete_result.status_code, 404)

    def test_to_check_recipe_search_success(self):
        """ Method to check for success in searching for a recipe item
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)
        create_another_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                                   headers=dict(Authorization=self.access_token),
                                                   data=self.other_recipes)
        self.assertEqual(create_another_recipe.status_code, 201)

        get_created_recipe = self.client().get(
            base_url + '/categories/1/recipes/search/?q=Another_New_Recipes',
            headers=dict(Authorization=self.access_token))
        self.assertEqual(get_created_recipe.status_code, 200)

    def test_to_check_for_null_item_provided_for_search(self):
        """ Method to check for no recipe search item provided
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)
        create_another_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                                   headers=dict(Authorization=self.access_token),
                                                   data=self.other_recipes)
        self.assertEqual(create_another_recipe.status_code, 201)

        get_created_recipe = self.client().get(
            base_url + '/categories/1/recipes/search/?q&page&limit',
            headers=dict(Authorization=self.access_token))
        self.assertEqual(get_created_recipe.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()
