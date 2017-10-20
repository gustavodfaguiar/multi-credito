from multi_credit.db import db
from flask import request, jsonify, Blueprint
from multi_credit.user.models import User
from werkzeug.security import generate_password_hash
from multi_credit.security import token_required


user = Blueprint('user', __name__)


# GET /user/<int:user_id>
@user.route('/v1/user/<int:user_id>', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    return jsonify({'user': user.serialize}), 201


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
