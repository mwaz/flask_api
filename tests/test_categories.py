"""Class to test the Category class"""

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
        
        self.login_data = self.client().post('yummy_api/v1/auth/login', data=user_details,
        content_type="application/json")

        # login a user and obtain the token 
        self.access_token = json.loads(
            self.login_data.data.decode())['access_token']

    def test_create_categories(self):
        """Test if the API can create a recipe category using [post]
        """

        create_categories = self.client().post('/yummy_api/v1/categories/',
                                               headers=dict(Authorization="Bearer " + self.access_token),
                                               data=self.categories)
        self.assertEqual(create_categories.status_code, 201)
        # #Asserts that the new_category is the created category
        # self.assertIn('new_category', str(create_categories.data))

    def test_api_can_get_all_recipe_categories(self):
        """Test if the api can get all the recipe
        categories
         """
        get_categories = self.client().post('/yummy_api/v1/categories/', headers=dict(
            Authorization="Bearer " + self.access_token), data = self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get('/yummy_api/v1/categories/', headers=dict(
            Authorization="Bearer " + self.access_token))
        self.assertEqual(get_categories.status_code, 200)
        self.assertIn('new_category', str(get_categories.data))

    def test_api_can_get_category_by_id(self):
        """test to check if one can get the recipe category
         using provided ID
         """

        get_category_by_id=self.client().post('/yummy_api/v1/categories/', headers=dict(Authorization="Bearer " + self.access_token), data = self.categories)
        self.assertEqual(get_category_by_id.status_code, 201)
        get_result_in_json = json.loads(get_category_by_id.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/yummy_api/v1/categories/{}'.format(get_result_in_json['id']), headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(result.status_code, 200)
        #test to check if the returned category is the one in the first index
        self.assertIn('new_category', str(result.data))

    def test_api_can_edit_a_recipe_category(self):
        """test if API can edit a recipe category
        """
        create_category = self.client().post('/yummy_api/v1/categories/', headers=dict(Authorization="Bearer " + self.access_token), data={'category_name': 'new_category'})
        self.assertEqual(create_category.status_code, 201)

        edit_category = self.client().put('/yummy_api/v1/categories/1', headers=dict(Authorization="Bearer " + self.access_token), data={"category_name": "newly_edited_category"})
        self.assertEqual(edit_category.status_code, 200)

        #test to check whether the edited category exists
        results=self.client().get('/yummy_api/v1/categories/1', headers=dict(Authorization="Bearer " + self.access_token),)
        self.assertIn('newly_edited', str(results.data))

    def test_categories_deletion(self):
        """test API can delete a recipe category
        """
        create_category = self.client().post('/yummy_api/v1/categories/', headers=dict(Authorization="Bearer " + self.access_token), data={'category_name': 'new_category_name'})
        self.assertEqual(create_category.status_code, 201)

        delete_result = self.client().delete('/yummy_api/v1/categories/1', headers=dict(Authorization="Bearer " + self.access_token),)
        self.assertEqual(delete_result.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables
        """
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()










