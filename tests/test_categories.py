import unittest
import os
import json
from app import make_app, db

class CategoriesTestCase(unittest.TestCase):
    """Represents the test case for Categories"""

    def setUp(self):
        """Defines the initialization variables for the class"""
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.Categories = {'category_name' : 'new_category'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_categories(self):
        """Test if the API can create a recipe category using [post]"""
        create_categories = self.client.post('/categories/', data = self.categories)
        self.assertEqual(create_categories.status_code, 201)
        self.assertIn('new_category', str(create_categories.data))

    








