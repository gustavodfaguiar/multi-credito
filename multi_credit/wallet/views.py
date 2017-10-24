from multi_credit.db import db
from flask import jsonify, Blueprint, request
from multi_credit.wallet.models import Wallet
from multi_credit.card.models import Card
from multi_credit.security import token_required


wallet = Blueprint('wallet', __name__)


# GET /wallet
@wallet.route('/v1/wallet', methods=['GET'])
@token_required
def get_wallet(current_user):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    return jsonify({'wallet': wallet.serialize}), 201


# PUT /wallet
@wallet.route('/v1/wallet', methods=['PUT'])
@token_required
def update_limit_wallet(current_user):
    wallet = Wallet.query.filter_by(
        user_id=current_user.id).first()

    if request.json.get('user_limit') > wallet.max_limit:
        return jsonify({'message': "Passed the limit!"}), 200

    wallet.user_limit = request.json.get('user_limit')
    db.session.commit()

    return jsonify({'message': "Updated limit wallet!"}), 201
