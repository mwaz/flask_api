import unittest
import json
from app import make_app, db

class CategoriesTestCase(unittest.TestCase):
    """Represents the test case for Categories"""

    def setUp(self):
        """Defines the initialization variables for the class"""
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.categories = {'category_name' : 'new_category'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_categories(self):
        """Test if the API can create a recipe categ
        ory using [post]"""
        create_categories = self.client().post('/flask_api/v1/categories/',
                                               data = self.categories)
        self.assertEqual(create_categories.status_code, 201)
        self.assertIn('new_category', str(create_categories.data))

    def test_api_can_get_all_recipe_categories(self):
        """Test if the api can get all the recipe categories"""
        get_categories = self.client().post('/flask_api/v1/categories/', data = self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().post('/categories/')
        self.assertEqual(get_categories.status_code, 200)
        self.assertIn('new_category', str(get_categories.data))

    def test_api_can_get_category_by_id(self):
        """test to check if one can get the recipe category using provided ID"""
        get_category_by_id = self.client().post('/flask_api/v1/categories/', data = self.categories)
        self.assertEqual(get_category_by_id.status_code, 201)
        get_result_in_json = json.loads(get_category_by_id.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/categories/{}'.format(get_result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('new_category', str(result.data))

    def test_api_can_edit_a_recipe_category(self):
        """test if API can edit a recipe category"""
        create_category = self.client().post('/flask_api/v1/categories/', data={'category_name': 'new_category'})
        self.assertEqual(create_category.status_code, 201)

        edit_category = self.client().put('/flask_api/v1/categories/1', data={"category_name": "newly_edited_category"})
        self.assertEqual(edit_category.status_code, 200)
        results = self.client().get('/flask_api/v1/categories/1')
        self.assertIn('newly_edited', str(results.data))

    def test_categories_deletion(self):
        """test API can delete a recipe category"""
        create_category = self.client().post('/categories/', data={'category_name': 'new_category_name'})
        self.assertEqual(create_category.status_code, 201)

        delete_result = self.client().delete('/flask_api/v1/categories/1')
        self.assertEqual(delete_result.status_code, 200)

        # Test to see if the deleted category still exists, if not a 404 should be returned
        result_if_category_exists = self.client().get('/flask_api/v1/categories/1')
        self.assertEqual(result_if_category_exists.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()










