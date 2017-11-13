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

   






