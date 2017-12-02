import unittest
from app import make_app, db
import json

class RecipesTestCase(unittest.TestCase):
    """Class to test, creation, deletion and editing recipes"""
    def setUp(self):
        """method to define varibles to be used in the tests"""
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.recipes = {'recipe_name': 'new_recipes',
                        'recipe_ingredients' : 'milk',
                        'recipe_methods': 'boil to heat'}

        #binds app to the current context
        with self.app.app_context():
            #creates all the tables
            db.create_all()

    def test_to_create_recipe(self):
        """test method to create a recipe"""
        create_recipe = self.client().post('/flask_api/v1/recipes', data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        get_created_recipe = self.client().get('/flask_api/v1/recipes/')
        self.assertIn('new_recipe', str(get_created_recipe.data))

    def test_to_get_all_recipes(self):
        """Test method to get all recipes"""
        create_recipe = self.client().post('/flask_api/v1/recipes/', data=self.recipes)
        self.assertEqual(create_recipe.status_code, 201)

        get_created_recipe = self.client().get('/flask_api/v1/recipes/')
        self.assertEqual(get_created_recipe.data, 200)
        self.assertIn('new_recipe', str(get_created_recipe.data))

    def test_to_edit_a_recipe_name(self):
        """Test to edit a recipe name"""
        create_recipe = self.client().post('/flask_api/v1/recipes/', data={'recipe_name': 'new_recipe_name',
                                                                           'recipe_ingredients' : 'milk',
                                                                           'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 201)
        
        edit_recipe = self.client().put('/flask_api/v1/recipes/1', data={'recipe_name': 'new_recipe_name',
                                                                           'recipe_ingredients' : 'milk',
                                                                           'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)
        get_edited_recipe = self.client().get('/flask_api/v1/recipes/1')
        self.assertIn('edited_recipe_name', get_edited_recipe.data)

    def test_to_edit_recipe_ingredients(self):
        """Test to chec the edit_recipe_ingredients functionality"""
        create_recipe = self.client().post('/flask_api/v1/recipes/', data={'recipe_name': 'new_recipe_name',
                                                                           'recipe_ingredients' : 'milk',
                                                                           'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put('/flask_api/v1/recipes/1', data={'recipe_name': 'new_recipe_name',
                                                                         'recipe_ingredients' : 'Butter',
                                                                         'recipe_methods': 'boil to heat'})
        self.assertEqual(edit_recipe.status_code, 201)
        get_edited_recipe = self.client().get('/flask_api/v1/recipes/1')
        self.assertIn('Butter', get_edited_recipe.data)

    def test_to_edit_recipe_preparation(self):
        """Test to check the edit recipe preparation method functionality"""
        create_recipe = self.client().post('/flask_api/v1/recipes/', data={'recipe_name': 'new_recipe_name',
                                                                           'recipe_ingredients' : 'milk',
                                                                           'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 201)

        edit_recipe = self.client().put('/flask_api/v1/recipes/1', data={'recipe_name': 'new_recipe_name',
                                                                         'recipe_ingredients' : 'Butter',
                                                                         'recipe_methods': 'warm till ready'})
        self.assertEqual(edit_recipe.status_code, 201)
        get_edited_recipe = self.client().get('/flask_api/v1/recipes/1')
        self.assertIn('warm till ready', get_edited_recipe.data)

    def test_to_get_recipe_by_id(self):
        """Test to get a single recipe using the recipe id"""
        create_recipe = self.client().post('/flask_api/v1/recipes/', data={'recipe_name': 'new_recipe_name',
                                                                           'recipe_ingredients': 'milk',
                                                                           'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 201)
        get_recipe = self.client().get('/flask_api/v1/recipes/1')
        self.assertEqual(get_recipe.status_code, 200)
        self.assertIn('new_recipe_name', str(get_recipe.data))

    def recipe_delete_by_id(self):
        create_recipe = self.client().post('/flask_api/v1/recipes/', data={'recipe_name': 'new_recipe_name',
                                                                           'recipe_ingredients': 'milk',
                                                                           'recipe_methods': 'boil to heat'})
        self.assertEqual(create_recipe.status_code, 201)

        delete_result = self.client().delete('/flask_api/v1/recipes/1')
        self.assertEqual(delete_result.status_code, 200)

        # Test to see if the deleted category still exists, if not a 404 should be returned
        result_if_recipe_exists = self.client().get('/flask_api/v1/recipes/1')
        self.assertEqual(result_if_recipe_exists.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()





        


