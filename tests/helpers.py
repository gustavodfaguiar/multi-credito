import json


def create_user(self):
    response = self.client.post(
        '/api/v1/user',
        data=json.dumps(self.user_data),
        headers=self.headers)
    return response


def sign_in(self):
    response = self.client.get(
        '/api/v1/login',
        data=json.dumps(self.user_login),
        headers=self.headers)
    return response
