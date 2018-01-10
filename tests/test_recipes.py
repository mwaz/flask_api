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
        """method to define variables to be used in the tests
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

        with self.app.app_context():

            db.create_all()

        # register a user
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
                           headers=dict(Authorization=self.access_token),
                           data=self.categories)

    def test_to_check_successful_recipe_creation(self):
        """test method to check successfully created recipe
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data={"recipe_name": "New_Recipe",
                                 "recipe_ingredients": "milk",
                                 "recipe_methods": "heat to boil"})

        get_created_recipe = self.client().get(base_url + '/categories/1/recipes/',
                                               headers=dict(Authorization=self.access_token))
        self.assertIn('New_Recipe', str(get_created_recipe.data))
        self.assertEqual(get_created_recipe.status_code, 200)

    def test_null_recipe_name_on_recipe_creation(self):
        """test if recipe name is null when creating a recipe
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": " ",
                                                 "recipe_ingredients": "milk",
                                                 "recipe_methods": "heat to boil"})
        self.assertEqual(create_recipe.status_code, 400)
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'], 'recipe name cannot be empty or with invalid characters')

    def test_null_recipe_methods_on_recipe_creation(self):
        """test if recipe methods are null when creating a recipe
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "New Recipe",
                                                 "recipe_ingredients": "milk",
                                                 "recipe_methods": " "})

        self.assertEqual(create_recipe.status_code, 400)
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'],
                      'Kindly provide ingredients and methods')

    def test_null_recipe_ingredients_on_recipe_creation(self):
        """test if recipe ingredients are null when creating a recipe
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "New Recipe",
                                                 "recipe_ingredients": "",
                                                 "recipe_methods": "heat to boil"})

        self.assertEqual(create_recipe.status_code, 400)
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'],
                      'Kindly provide ingredients and methods')

    def test_invalid_recipe_name_on_recipe_creation(self):
        """test if recipe name is valid when creating a recipe
        """
        create_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                           headers=dict(Authorization=self.access_token),
                                           data={"recipe_name": "",
                                                 "recipe_ingredients": "milk, water",
                                                 "recipe_methods": "heat to boil"})
        recipe_data = json.loads(create_recipe.data.decode())
        self.assertIn(recipe_data['message'], 'recipe name cannot be empty or with invalid characters')
        self.assertEqual(create_recipe.status_code, 400)

    def test_duplicate_recipe_on_recipe_creation(self):
        """test if recipe is duplicated when trying to create a recipe
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data={'recipe_name': 'New_Recipes',
                                 'recipe_ingredients': 'milk',
                                 'recipe_methods': 'boil to heat'})

        create_another_recipe = self.client().post(base_url + '/categories/1/recipes/',
                                                   headers=dict(Authorization=self.access_token),
                                                   data=self.recipes)

        self.assertEqual(create_another_recipe.status_code, 400)
        recipe_data = json.loads(create_another_recipe.data.decode())
        self.assertIn(recipe_data['message'], 'Recipe name exists')

    def test_non_existent_category_when_creating_a_recipe(self):
        """test failure in creating a recipe
        in a category that does not exist
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
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.other_recipes)

        get_created_recipe = self.client().get(base_url + '/categories/1/recipes/?page=1&limit=1',
                                               headers=dict(Authorization=self.access_token))
        self.assertEqual(get_created_recipe.status_code, 200)

    def test_to_check_success_edit_of_a_recipe_name(self):
        """Test to check success when editing a recipe name
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'edited_recipe_name',
                                              'recipe_ingredients': 'milk, milk',
                                              'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_edit_recipe_with_null_name(self):
        """Test to edit a recipe with a null recipe name
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)

        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': '',
                                              'recipe_ingredients': 'milk, milk',
                                              'recipe_methods': 'boil to heat'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'], 'recipe name cannot be empty or with invalid characters')

    def test_to_edit_recipe_with_null_recipe_methods(self):
        """Test to edit a recipe with null recipe methods
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipes',
                                              'recipe_ingredients': 'milk, milk',
                                              'recipe_methods': ''})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'],
                      'Kindly provide ingredients and methods')

    def test_to_edit_recipe_with_null_recipe_ingredients(self):
        """Test to edit a recipe with null recipe ingredients
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipes',
                                              'recipe_ingredients': '',
                                              'recipe_methods': 'heat to boil'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'],
                      'Kindly provide ingredients and methods')

    def test_edit_invalid_recipe_name(self):
        """Test to edit a recipe with an invalid recipe name
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': '@@@@##$',
                                              'recipe_ingredients': 'ingredients here',
                                              'recipe_methods': 'heat to boil'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 400)
        self.assertIn(category_data['message'], 'recipe name cannot be empty or with invalid characters')

    def test_edit_non_existent_recipe(self):
        """Test to edit a non-existent recipe
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        edit_recipe = self.client().put(base_url + '/categories/1/recipes/2',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'new recipe name',
                                              'recipe_ingredients': 'ingredients here',
                                              'recipe_methods': 'heat to boil'})
        category_data = json.loads(edit_recipe.data.decode())
        self.assertEqual(edit_recipe.status_code, 404)
        self.assertIn(category_data['message'], 'No recipe found')

    def test_to_check_a_successful_edit_recipe_ingredients(self):
        """Test to check the success editing the ingredients of a recipe
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipe_name',
                                              'recipe_ingredients': 'Butter',
                                              'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_check_successful_edit_on_recipe_preparation(self):
        """Test to check the successful
        editing of the preparation of a recipe
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        edit_recipe = self.client().put(base_url + '/categories/1/recipes/1',
                                        headers=dict(Authorization=self.access_token),
                                        data={'recipe_name': 'New_Recipe_name',
                                              'recipe_ingredients': 'Butter',
                                              'recipe_methods': 'warm till ready'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_get_a_recipe_by_id(self):
        """Test to get a single recipe using the recipe id
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        get_recipe = self.client().get(base_url + '/categories/1/recipes/1',
                                       headers=dict(Authorization=self.access_token))
        self.assertIn('New_Recipes', str(get_recipe.data))

    def test_to_check_non_existent_recipe_id_on_get(self):
        """Test to check for a non existent recipe id on get
        """
        get_recipe = self.client().get(base_url + '/categories/1/recipes/2',
                                       headers=dict(Authorization=self.access_token))
        recipe_data = json.loads(get_recipe.data.decode())
        self.assertEqual(get_recipe.status_code, 404)
        self.assertIn(recipe_data['message'], 'No recipe found')

    def test_success_recipe_delete_by_id(self):
        """Method to test success in  deleting a recipe by id
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)

        delete_result = self.client().delete(base_url + '/categories/1/recipes/1',
                                             headers=dict(Authorization=self.access_token))
        self.assertEqual(delete_result.status_code, 200)

    def test_check_recipe_double_delete(self):
        """Method to test double recipe delete
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        self.client().delete(base_url + '/categories/1/recipes/1',
                             headers=dict(Authorization=self.access_token))

        delete_result = self.client().delete(base_url + '/categories/1/recipes/1',
                                             headers=dict(Authorization=self.access_token))
        self.assertEqual(delete_result.status_code, 404)

    def test_to_check_recipe_search_success(self):
        """ Method to check for success in searching for a recipe item
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.other_recipes)
        get_created_recipe = self.client().get(
            base_url + '/recipes/search/?q=Another_New_Recipes',
            headers=dict(Authorization=self.access_token))
        self.assertEqual(get_created_recipe.status_code, 200)

    def test_to_check_for_null_name_provided_for_recipe_search(self):
        """ Method to check for no recipe search item provided
        """
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.recipes)
        self.client().post(base_url + '/categories/1/recipes/',
                           headers=dict(Authorization=self.access_token),
                           data=self.other_recipes)
        get_created_recipe = self.client().get(
            base_url + '/recipes/search/?q&page&limit',
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
