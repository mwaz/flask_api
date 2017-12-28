"""Class to test the Category class methods
"""

import unittest
import json
from app import make_app, db

base_url = '/yummy_api/v1/'


class CategoriesTestCase(unittest.TestCase):
    """Represents the test case for Categories
    """

    def setUp(self):
        """Defines the initialization variables for the class
        """
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.categories = {'category_name': 'New_Category'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        #register a user
        user_details = json.dumps(dict({
            "email": "test@test.com",
            "password": "password",
            "username": "User",
            "secret_word": "TOP SECRET"
        }))
        self.client().post(base_url + 'auth/register', data=user_details,
                           content_type="application/json")

        # Login  a test user
        login_details = json.dumps(dict({
            "email": "test@test.com",
            "password": "password"
        }))

        self.login_data = self.client().post(base_url + 'auth/login', data=user_details,
                                             content_type="application/json")

        # login a user and obtain the token
        self.access_token = json.loads(
            self.login_data.data.decode())['access_token']

    def test_create_categories(self):
        """Test if the API can create a recipe category using [post]
        """
        create_categories = self.client().post(base_url + 'categories/',
                                               headers=dict(
                                                   Authorization=self.access_token),
                                               data=self.categories)
        self.assertEqual(create_categories.status_code, 201)

    def test_null_category_name(self):
        """Method to test failure in creating a category
        """
        create_categories = self.client().post(base_url + 'categories/',
                                               headers=dict(
                                                   Authorization=self.access_token),
                                               data={'category_name': ''})
        categories_data = json.loads(create_categories.data.decode())
        self.assertEqual(create_categories.status_code, 400)
        self.assertIn(categories_data['message'], 'category name not provided')

    def test_invalid_category_name(self):
        """Method to test invalid category name
        """
        create_categories = self.client().post(base_url + 'categories/',
                                               headers=dict(
                                                   Authorization=self.access_token),
                                               data={'category_name': '@@@@@'})
        categories_data = json.loads(create_categories.data.decode())
        self.assertEqual(create_categories.status_code, 400)
        self.assertIn(categories_data['message'], 'Category name is not valid')

    def test_existing_category_name(self):
        """Method to test an existing category name
        """
        create_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(create_categories.status_code, 201)

        create_duplicate_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        category_data = json.loads(create_duplicate_categories.data.decode())
        self.assertEqual(create_duplicate_categories.status_code, 400)
        self.assertIn(category_data['message'], 'Category name exists')

    def test_api_can_get_all_recipe_categories(self):
        """Test if the api can get all the recipe categories
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 200)

    def test_to_check_for_invalid_page_number_on_category_fetch(self):
        """Method to test invalid arguements of page on category fetch
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/?page=fd', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 400)

    def test_to_check_for_invalid_limit_parameter_on_category_fetch(self):
        """Method to test invalid arguements of limit on category fetch
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/?limit=fd', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 400)

    def test_to_check_for_paginated_recipe_categories(self):
        """Method to test pagination of category results
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/?page=1&limit=1', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 200)

    def test_to_check_response_from_url_parameters(self):
        """Method to check returned response of an empty category
        """
        get_categories = self.client().get(base_url + 'categories/?page=1435&limit=1342', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 404)

    def test_api_can_get_category_by_id(self):
        """test to check if one can get the recipe category
        using provided ID
        """
        get_category_by_id = self.client().post(base_url + 'categories/',
                                                headers=dict(Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_category_by_id.status_code, 201)
        get_result_in_json = json.loads(
            get_category_by_id.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            base_url + 'categories/{}'.format(get_result_in_json['id']), headers=dict(Authorization=self.access_token))
        self.assertEqual(result.status_code, 200)
        category_data = json.loads(result.data.decode())
        #test to check if the returned category is the one in the first index
        self.assertIn('New_Category', category_data['category_name'])

    def test_api_failure_to_get_a_category(self):
        """test to check error failure if category not found
        """
        get_category_by_id = self.client().post(base_url + 'categories/',
                                                headers=dict(Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_category_by_id.status_code, 201)
        result = self.client().get(base_url + 'categories/2',
                                   headers=dict(Authorization=self.access_token))
        get_result_in_json = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 404)
        self.assertIn(get_result_in_json['message'], 'No Category Found')

    def test_api_can_edit_a_recipe_category(self):
        """test if API can edit a recipe category
        """
        create_category = self.client().post(base_url + 'categories/',
                                             headers=dict(Authorization=self.access_token), data={'category_name': 'New_Category'})
        self.assertEqual(create_category.status_code, 201)

        edit_category = self.client().put(base_url + 'categories/1', headers=dict(
            Authorization=self.access_token), data={"category_name": "newly_edited_category"})
        self.assertEqual(edit_category.status_code, 200)

        #test to check whether the edited category exists
        results = self.client().get(base_url + 'categories/1',
                                    headers=dict(Authorization=self.access_token))
        category_data = json.loads(results.data.decode())
        self.assertIn('Newly_Edited', category_data['category_name'])

    def test_api_can_edit_a_recipe_category_that_does_not_exist(self):
        """test if API can edit a recipe category that does not exist
        """
        edit_category = self.client().put(base_url + 'categories/1', headers=dict(
            Authorization=self.access_token), data={"category_name": "newly_edited_category"})
        self.assertEqual(edit_category.status_code, 404)

    def test_edit_category_with_null_name(self):
        """test if API can edit a recipe category with a null name
        """
        create_category = self.client().post(base_url + 'categories/',
                                             headers=dict(Authorization=self.access_token), data={'category_name': 'New_Category'})
        self.assertEqual(create_category.status_code, 201)

        edit_category = self.client().put(base_url + 'categories/1',
                                          headers=dict(Authorization=self.access_token), data={"category_name": ""})
        self.assertEqual(edit_category.status_code, 400)
        category_data = json.loads(edit_category.data.decode())
        self.assertIn(category_data['message'], 'category name not provided')

    def test_edit_category_with_invalid_name(self):
        """test if API can edit a recipe category with an invalid name
        """
        create_category = self.client().post(base_url + 'categories/',
                                             headers=dict(Authorization=self.access_token), data={'category_name': 'New_Category'})
        self.assertEqual(create_category.status_code, 201)

        edit_category = self.client().put(base_url + 'categories/1',
                                          headers=dict(Authorization=self.access_token), data={"category_name": "@@@@"})
        self.assertEqual(edit_category.status_code, 400)
        category_data = json.loads(edit_category.data.decode())
        self.assertIn(category_data['message'], 'Category name is not valid')

    def test_edit_category_with_existing_category_name(self):
        """test if API can edit a recipe category with an existing category name
        """
        create_category = self.client().post(base_url + 'categories/',
                                             headers=dict(Authorization=self.access_token), data={'category_name': 'New_Category'})
        self.assertEqual(create_category.status_code, 201)

        edit_category = self.client().put(base_url + 'categories/1',
                                          headers=dict(Authorization=self.access_token), data={"category_name": "New_Category"})
        self.assertEqual(edit_category.status_code, 400)
        category_data = json.loads(edit_category.data.decode())
        self.assertIn(category_data['message'], 'Category name exists')

    def test_categories_deletion(self):
        """test API can delete a recipe category
        """
        create_category = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data={'category_name': 'New_Category_name'})
        self.assertEqual(create_category.status_code, 201)

        delete_result = self.client().delete(base_url + 'categories/1',
                                             headers=dict(Authorization=self.access_token),)
        self.assertEqual(delete_result.status_code, 200)

    def test_categories_deletion(self):
        """test API can not delete a recipe category twice
        """
        create_category = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data={'category_name': 'New_Category_name'})
        self.assertEqual(create_category.status_code, 201)

        delete_result = self.client().delete(base_url + 'categories/1',
                                             headers=dict(Authorization=self.access_token),)
        self.assertEqual(delete_result.status_code, 200)

        delete_result = self.client().delete(base_url + 'categories/1',
                                             headers=dict(Authorization=self.access_token),)
        self.assertEqual(delete_result.status_code, 404)

    def test_to_check_for_paginated_searched_recipe_categories(self):
        """Method to test pagination of searched category results
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/search/?q=New&page=1&limit=1', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 200)

    def test_to_check_null_search_response(self):
        """Method to check returned response of an empty category
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/search/?q=cate', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 200)

    def test_to_check_for_invalid_page_number_on_search(self):
        """Method to test invalid arguements on category search
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/search/?q=New&page=fd', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 400)

    def test_to_check_for_invalid_limit_parameter_on_search(self):
        """Method to test pagination of searched category results
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/search/?q=New&limit=fd', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 400)

    def test_to_search_with_null_category_item(self):
        """Test to search with no category item provided
        """
        get_categories = self.client().post(base_url + 'categories/', headers=dict(
            Authorization=self.access_token), data=self.categories)
        self.assertEqual(get_categories.status_code, 201)
        get_categories = self.client().get(base_url + 'categories/search/', headers=dict(
            Authorization=self.access_token))
        self.assertEqual(get_categories.status_code, 200)

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
