from flask import jsonify, Blueprint
from multi_credit.wallet.models import Wallet
from multi_credit.security import token_required


wallet = Blueprint('wallet', __name__)


# GET /wallet
@wallet.route('/v1/wallet', methods=['GET'])
@token_required
def get_wallet(current_user):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    return jsonify({'wallet': wallet.serialize}), 201
