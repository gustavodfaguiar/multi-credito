import json


class TestHelper:

    headers = {
        'content-type': 'application/json',
        'authorization': 'Basic Z3VzdGF2b0BnbWFpbC5jb206MTIzNDU2',
        'x-access-token': ''
    }

    user = {
        "name": "Gustavo Dirceu Faria Aguiar",
        "email": "gustavo@gmail.com",
        "password": "123456"
    }

    login = {
        "username": "gustavo@gmail.com",
        "password": "123456"
    }

    def create_user(self, client):
        response = client.post(
            '/api/v1/user',
            data=json.dumps(self.user),
            headers=self.headers)
        return response

    def sign_in(self, client):
        response = client.get(
            '/api/v1/login',
            data=json.dumps(self.login),
            headers=self.headers)
        return response
