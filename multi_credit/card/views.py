from multi_credit.db import db
from flask import request, jsonify, Blueprint
from multi_credit.card.models import Card
from multi_credit.wallet.models import Wallet
from multi_credit.security import token_required
from datetime import datetime


card = Blueprint('card', __name__)


# POST /card data: {number, expiration_date, validity_date,
#            name, cvv, limit, credit, wallet_id}
@card.route("/v1/card", methods=['POST'])
@token_required
def create_card(current_user):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    request_data = request.get_json()
    format_expiration_date = datetime.strptime(
        request_data['expiration_date'].replace("-", ""), "%Y%m%d").date()

    format_validity_date = datetime.strptime(
        request_data['expiration_date'].replace("-", ""), "%Y%m%d").date()

    new_card = Card(
        number=request_data['number'],
        expiration_date=format_expiration_date,
        validity_date=format_validity_date,
        name=current_user.name_card,
        cvv=request_data['cvv'],
        limit=request_data['limit'],
        credit=request_data['limit'],
        wallet_id=wallet.id
    )

    try:
        db.session.add(new_card)
        db.session.commit()
    except:
        return jsonify({'message': 'Card already exists!'}), 200

    return jsonify({'message': 'New card created!'}), 201
