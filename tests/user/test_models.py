from multi_credit import app, db
import unittest
import json
from tests.helpers import TestHelper


class UserModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_create_user(self):
        response = TestHelper().create_user(self.client)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], "New user created!")
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        TestHelper().create_user(self.client)
        response = TestHelper().create_user(self.client)
        result = json.loads(response.data.decode())

        self.assertEqual(
            result['message'], "User already exists!")
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        TestHelper().create_user(self.client)
        response = TestHelper().sign_in(self.client)
        self.assertEqual(response.status_code, 201)

    def test_get_one_user(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        response_get_user = self.client.get(
            '/api/v1/user',
            headers=headers)

        self.assertEqual(response_get_user.status_code, 201)
