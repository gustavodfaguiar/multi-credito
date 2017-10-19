from multi_credit.user.models import User
from multi_credit import app, db
import unittest
import json


class UserModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.headers = {'content-type': 'application/json'}
        self.user_data = {
            "name": "Gustavo Dirceu Faria Aguiar",
            "email": "gustavo@gmail.com",
            "password": "123456"
        }

        with self.app.app_context():
            db.create_all()

    def test_create_user(self):
        response = self.client.post(
            '/api/v1/user',
            data=json.dumps(self.user_data),
            headers=self.headers)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], "New user created!")
        self.assertEqual(response.status_code, 201)
