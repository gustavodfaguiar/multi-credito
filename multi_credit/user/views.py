from multi_credit.db import db
from flask import request, jsonify, Blueprint
from multi_credit.user.models import User
from werkzeug.security import generate_password_hash


user = Blueprint('user', __name__)


# POST /user data: {name, email, password}
@user.route("/v1/user", methods=['POST'])
def create_user():
    request_data = request.get_json()

    hashed_password = generate_password_hash(
                request_data['password'], method='sha256')

    new_user = User(name=request_data['name'],
                    email=request_data['email'],
                    password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201
