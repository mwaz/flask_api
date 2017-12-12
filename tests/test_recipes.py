"""Base Class to test recipe.py class"""
import json
import unittest
from app import make_app, db


class RecipesTestCase(unittest.TestCase):
    """Class to test, creation, deletion and editing recipes"""
    def setUp(self):
        """method to define varibles to be used in the tests"""
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.recipes = {'recipe_name': 'new_recipes',
                        'recipe_ingredients' : 'milk',
                        'recipe_methods': 'boil to heat'}
        self.categories = {'category_name' : 'new_category'}

        #binds app to the current context
        with self.app.app_context():
            #creates all the tables
            db.create_all()

        #register a user 
        user_details = json.dumps(dict({
            "email": "test@test.com",
            "password": "password"
            }))
        self.client().post('yummy_api/v1/auth/register', data=user_details,
                           content_type="application/json")
        
        # Login  a test user 
        login_details = json.dumps(dict({
            "email": "test@test.com",
            "password": "password"
            }))

        self.login_data = self.client().post('yummy_api/v1/auth/login', data=login_details,
                                             content_type="application/json")
        
        # login a user and obtain the token 
        self.access_token = json.loads(
            self.login_data.data.decode())['access_token']

        # create a category
        create_category = self.client().post('/yummy_api/v1/categories/',
                                             headers=dict(Authorization="Bearer " + self.access_token),
                                             data=self.categories)

      

    def test_to_create_recipe(self):
        """test method to create a recipe"""

        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/', 
                                           headers=dict(Authorization="Bearer " + 
                                                        self.access_token), data={"recipe_name": "new_recipe",
                                                                     "recipe_ingredients": "milk", 
                                                                     "recipe_methods": "heat to boil"})

        self.assertEqual(create_recipe.status_code, 201)

        get_created_recipe = self.client().get('/yummy_api/v1/categories/1/recipes/',
                                               headers=dict(Authorization="Bearer " +
                                                            self.access_token))
        self.assertIn('new_recipe', str(get_created_recipe.data))

    def test_to_get_all_recipes(self):
        """Test method to get all recipes"""
        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/', 
                                           headers=dict(Authorization="Bearer " + 
                                                        self.access_token), data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)
        create_another_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/',
                                                   headers=dict(Authorization="Bearer " +
                                                                self.access_token), data=self.recipes)
        self.assertEqual(create_another_recipe.status_code, 201)

        get_created_recipe = self.client().get('/yummy_api/v1/categories/1/recipes/',
                                               headers=dict(Authorization="Bearer " +
                                                            self.access_token))
        self.assertEqual(get_created_recipe.status_code, 200)

    def test_to_edit_a_recipe_name(self):
        """Test to edit a recipe name"""
        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/',
                                           headers=dict(Authorization="Bearer " +
                                                        self.access_token), data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put('/yummy_api/v1/categories/1/recipes/1',
                                        headers=dict(Authorization="Bearer " +
                                                     self.access_token),data={'recipe_name': 'edited_recipe_name',
                                                                 'recipe_ingredients' : 'milk, milk',
                                                                 'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)
     

    def test_to_edit_recipe_ingredients(self):
        """Test to chec the edit_recipe_ingredients functionality
        """
        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/',
                                           headers=dict(Authorization="Bearer " +
                                                        self.access_token), data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put('/yummy_api/v1/categories/1/recipes/1',
                                        headers=dict(Authorization="Bearer " +
                                                     self.access_token),data={'recipe_name': 'new_recipe_name',
                                                                         'recipe_ingredients' : 'Butter',
                                                                         'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)

    def test_to_edit_recipe_preparation(self):
        """Test to check the edit recipe preparation method functionality
        """
        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/',
                                           headers=dict(Authorization="Bearer " +
                                           self.access_token), data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put('/yummy_api/v1/categories/1/recipes/1',
                                        headers=dict(Authorization="Bearer " +
                                        self.access_token), data={'recipe_name': 'new_recipe_name',
                                                                         'recipe_ingredients' : 'Butter',
                                                                         'recipe_methods': 'warm till ready'})
        self.assertEqual(edit_recipe.status_code, 201)
    def test_to_get_recipe_by_id(self):
        """Test to get a single recipe using the recipe id
        """
        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/',
                                           headers=dict(Authorization="Bearer " +
                                                        self.access_token), data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)
        
        get_recipe = self.client().get('/yummy_api/v1/categories/1/recipes/1',
                                       headers=dict(Authorization="Bearer " +
                                                    self.access_token))
        # self.assertEqual(get_recipe.status_code, 200)
        self.assertIn('new_recipes', str(get_recipe.data))

    def test_recipe_delete_by_id(self):
        """Method to test recipe delete by id
        """
        create_recipe = self.client().post('/yummy_api/v1/categories/1/recipes/',
                                           headers=dict(Authorization="Bearer " +
                                                        self.access_token), data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)
       
        delete_result = self.client().delete('/yummy_api/v1/categories/1/recipes/1',
                                             headers=dict(Authorization="Bearer " +
                                                          self.access_token))
        self.assertEqual(delete_result.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()





        


