from multi_credit.db import db
from flask import request, jsonify, Blueprint
from multi_credit.user.models import User
from multi_credit.wallet.models import Wallet
from werkzeug.security import generate_password_hash
from multi_credit.security import token_required


user = Blueprint('user', __name__)


# GET /user/<int:user_id>
@user.route('/v1/user', methods=['GET'])
@token_required
def get_one_user(current_user):
    user = User.query.filter_by(id=current_user.id).first()

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

    try:
        db.session.add(new_user)
        db.session.flush()
    except:
        return jsonify({'message': 'User already exists!'}), 200

    Wallet().create_wallet(new_user.id)

    return jsonify({'message': 'New user created!'}), 201
