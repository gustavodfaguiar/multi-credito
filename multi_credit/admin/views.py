from flask import request, make_response, Blueprint, jsonify
from multi_credit.user.models import User
from werkzeug.security import check_password_hash
import jwt
import datetime
import os

login = Blueprint('login', __name__)


# GET /login
@login.route('/v1/login', methods=['GET'])
def login_api():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'Could not verify', 401,
            {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response(
            'Could not verify', 401,
            {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        print('teste')
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
            os.environ.get('SECRET_KEY', 'secreta'))

        return jsonify({'token': token.decode('UTF-8')})

    return make_response(
        'Could not verify', 401,
        {'WWW-Authenticate': 'Basic realm="Login required!"'})
