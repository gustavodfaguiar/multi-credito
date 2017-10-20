from multi_credit.db import db
from flask import jsonify, Blueprint
from multi_credit.wallet.models import Wallet
from multi_credit.security import token_required


wallet = Blueprint('wallet', __name__)


# POST /wallet
@wallet.route("/v1/wallet", methods=['POST'])
@token_required
def create_wallet(current_user):

    new_wallet = Wallet(
        max_limit=0,
        user_limit=0,
        credit=0,
        user_id=current_user.id
    )

    try:
        db.session.add(new_wallet)
        db.session.commit()
    except:
        return jsonify({'message': 'Wallet already exists!'}), 200

    return jsonify({'message': 'New wallet created!'}), 201
