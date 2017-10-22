from multi_credit import app, db
import unittest
import json
from tests.helpers import create_user, sign_in


class UserModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
        self.client = self.app.test_client()
        self.headers = {
            'content-type': 'application/json',
            'authorization': 'Basic Z3VzdGF2b0BnbWFpbC5jb206MTIzNDU2',
            'x-access-token': ''
        }

        self.user_data = {
            "name": "Gustavo Dirceu Faria Aguiar",
            "email": "gustavo@gmail.com",
            "password": "123456"
        }

        self.user_login = {
            "username": "gustavo@gmail.com",
            "password": "123456"
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_create_user(self):
        response = create_user(self)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], "New user created!")
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        create_user(self)
        response = create_user(self)
        result = json.loads(response.data.decode())

        self.assertEqual(
            result['message'], "User already exists!")
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        create_user(self)
        response = sign_in(self)
        self.assertEqual(response.status_code, 201)

    def test_get_one_user(self):
        create_user(self)
        response_sign_in = sign_in(self)
        auth_token = json.loads(response_sign_in.data.decode())
        self.headers['x-access-token'] = auth_token['token']

        response_get_user = self.client.get(
            '/api/v1/user/1',
            headers=self.headers)

        self.assertEqual(response_get_user.status_code, 201)
