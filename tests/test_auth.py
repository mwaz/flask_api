"""Tests for User Authentication"""
import unittest
import json
from app import db, make_app

base_url = '/yummy_api/v1/auth'


class TestAuth(unittest.TestCase):
    """"Testcase for blueprint for authentication
    """

    def setUp(self):
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.user_details = {'email': 'someone@gmail.com',
                             'password': 'testing_p@ssword',
                             'username': 'new_user',
                             'secret_word': 'TOP SECRET'
                            }
        self.unathorized_user_details = {'email': 'uuser@unauthorized.com',
                                         'password': 'none_provided',
                                         'username': 'new_user',
                                         'secret_word': 'TOP SECRET'
                                        }
        self.password_reset_user_details = {'email': 'someone@gmail.com',
                                            'password': 'testing_reset_p@ssword',
                                            'secret_word': 'TOP SECRET'
                                           }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_register_user(self):
        """"Method to test a successful registration
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        result = json.loads(user_register.data.decode())
        self.assertEqual(result['message'], "Successfully registered")
        self.assertEqual(user_register.status_code, 201)

    def test_password_on_register(self):
        """Method to check for empty username or password strings on signup
        """
        user_register = self.client().post(base_url + '/register',
                                           data={'email': 'n@n.com', 'password': '4324', 'username': 'new',
                                                 'secret_word': 'secret'})
        self.assertEqual(user_register.status_code, 400)
        user_details = json.loads(user_register.data.decode())
        self.assertEqual(user_details['message'],
                         "Password should be more than six characters")

    def test_empty_secret_word_on_register(self):
        """Method to test for empty secret word on user register
        """
        user_register = self.client().post(
            base_url + '/register',
            data={'email': 'test@test.com', 'password': '32eq5646436rw',
                  'username': 'New_User', 'secret_word': ''})
        self.assertEqual(user_register.status_code, 400)
        user_details = json.loads(user_register.data.decode())
        self.assertEqual(user_details['message'],
                         "Kindly provide a SECRET word")

    def test_minimum_required_password_on_register(self):
        """Methdod to test for the minimum required password length on registration
        """
        user_register = self.client().post(
            base_url + '/register',
            data={'email': 'test@test.com', 'password': '32erw',
                  'username': 'New_User', 'secret_word': 'TOP SECRET'})
        self.assertEqual(user_register.status_code, 400)
        user_details = json.loads(user_register.data.decode())
        self.assertEqual(user_details['message'],
                         "Password should be more than six characters")

    def test_to_email_regex_pattern_on_register(self):
        """Method to check for a valid regex pattern on registration
        """
        user_register = self.client().post(base_url + '/register',
                                           data={'email': 't.com', 'password': '2324dsfscdsf',
                                                 'username': 'User', 'secret_word': 'TOP SECRET'})
        self.assertEqual(user_register.status_code, 400)

    def test_error_exception_on_user_register(self):
        """Method to check for error handling in registration
        """
        user_register = self.client().post(base_url + '/register',
                                           data={'emaill': 'test@test.com'})
        self.assertEqual(user_register.status_code, 400)

    def test_empty_email_and_password_on_login(self):
        """Method to check for empty email or password strings on login
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post(base_url + '/login',
                                        data={'email': '', 'password': ''})
        self.assertEqual(user_login.status_code, 400)
        user_details = json.loads(user_login.data.decode())
        self.assertEqual(user_details['message'],
                         "Error occurred on user login")

    def test_double_registration(self):
        """"Method to test a user who is already registered
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)
        double_user_registration = self.client().post(
            base_url + '/register', data=self.user_details)
        self.assertEqual(double_user_registration.status_code, 409)

    def test_user_login(self):
        """"Method to test successful user login
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post(base_url + '/login', data=self.user_details)
        self.assertEqual(user_login.status_code, 200)

    def test_unauthorized_login(self):
        """"Method to test unauthorized login
        """
        unauthorized_login = self.client().post(
            base_url + '/login', data=self.unathorized_user_details)
        self.assertEqual(unauthorized_login.status_code, 401)

    def test_to_check_empty_email_in_reset_password_in_auth(self):
        """Method to test for password reset
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)
        password_reset = self.client().put(
            base_url + '/password-reset',
            data={'email': '', 'reset_password': 'testing_reset_p@ssword',
                  'secret_word': 'TOP SECRET'})
        self.assertEqual(password_reset.status_code, 400)
        user_data = json.loads(password_reset.data.decode())
        self.assertIn(user_data['message'], "Invalid user email")

    def test_empty_reset_password(self):
        """Method to test for empty password while doing a password reset
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)
        password_reset = self.client().put(base_url + '/password-reset',
                                           data={'email': 'someone@gmail.com',
                                                 'reset_password': '', 'secret_word': 'TOP SECRET'})
        self.assertEqual(password_reset.status_code, 400)
        user_data = json.loads(password_reset.data.decode())
        self.assertIn(user_data['message'], "Kindly provide a reset Password")

    def test_to_check_success_in_reseting_password(self):
        """Method to check for successfully updated user password
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)
        password_reset = self.client().put(
            base_url + '/password-reset',
            data={'email': 'someone@gmail.com',
                  'reset_password': 'new_password', 'secret_word': 'TOP SECRET'})
        self.assertEqual(password_reset.status_code, 200)

    def test_user_logout(self):
        """Method to logout a user
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post(base_url + '/login', data=self.user_details)
        self.assertEqual(user_login.status_code, 200)

        # login a user and obtain the token
        self.access_token = json.loads(user_login.data.decode())[
            'access_token']

        user_logout = self.client().post(base_url + '/logout',
                                         headers=dict(Authorization=self.access_token))
        self.assertEqual(user_logout.status_code, 200)

    def test_error_exception_on_password_reset(self):
        """Method to check for a handled error exception on password reset
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)

        password_reset = self.client().put(base_url + '/password-reset',
                                           data={'emailll': 'someone@gmail.com',
                                                 'password': ''})
        self.assertEqual(password_reset.status_code, 400)

    def test_error_exception_on_user_login(self):
        """Method to test handled error exception on user login
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post(base_url + '/login',
                                        data={'emaigghl': 'someone@test.com',
                                              'passworrd': 'handled exception'})
        self.assertEqual(user_login.status_code, 400)

    def test_to_check_if_authorization_required_on_logout(self):
        """Method to test for authorizaton on user logout
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post(base_url + '/login', data=self.user_details)
        self.assertEqual(user_login.status_code, 200)

        # login a user and obtain the token
        self.access_token = json.loads(user_login.data.decode())[
            'access_token']

        user_logout = self.client().post(base_url + '/logout')
        self.assertEqual(user_logout.status_code, 401)

    def test_to_check_inexistent_user_email_on_password_reset(self):
        """test method to check condition if email does not exist on password reset
        """
        user_register = self.client().post(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)
        password_reset = self.client().put(
            base_url + '/password-reset',
            data={'email': 'someonee@gmail.com',
                  'reset_password': 'testing_p@ssword', 'secret_word': 'TOP SECRET'})
        self.assertEqual(password_reset.status_code, 404)
        password_reset_data = json.loads(password_reset.data.decode())
        self.assertIn(
            password_reset_data['message'], '"Kindly provide correct email and secret word"')

    def test_to_check_invalid_route(self):
        """test to check message returned after an invalid route is provided on register
        """
        user_register = self.client().post(base_url + '/register/', data=self.user_details)
        self.assertEqual(user_register.status_code, 404)
        register_data = json.loads(user_register.data.decode())
        self.assertIn(register_data['message'], 'Page not found')

    def test_invalid_method_on_route(self):
        """Method to check invalid route provided on register
        """
        user_register = self.client().get(base_url + '/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 405)
        register_data = json.loads(user_register.data.decode())
        self.assertIn(register_data['message'], 'Method not allowed')
