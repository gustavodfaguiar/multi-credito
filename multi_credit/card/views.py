from multi_credit.db import db
from flask import request, jsonify, Blueprint
from multi_credit.card.models import Card
from multi_credit.wallet.models import Wallet
from multi_credit.security import token_required
from datetime import datetime


card = Blueprint('card', __name__)


# GET /cards
@card.route('/v1/cards', methods=['GET'])
@token_required
def get_cards(current_user):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    cards = [card.serialize for card in Card.query.filter_by(
            wallet_id=wallet.id)]
    if not cards:
        return jsonify({'mensagem': 'No registration card!'})

    return jsonify({'cards': cards})


# GET /card/<int:card_id>
@card.route('/v1/card/<int:card_id>', methods=['GET'])
@token_required
def get_one_card(current_user, card_id):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    card = Card.query.filter_by(wallet_id=wallet.id, id=card_id).first()

    if not card:
        return jsonify({'message': 'No card found!'})

    return jsonify({'card': card.serialize})


# POST /card data: {number, expiration_date, validity_date,
#            name, cvv, limit, credit, wallet_id}
@card.route("/v1/card", methods=['POST'])
@token_required
def create_card(current_user):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    if not wallet:
        return jsonify({'message': 'No card found!'})

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


# DELETE /card/<int:card_id>
@card.route('/v1/card/<int:card_id>', methods=['DELETE'])
@token_required
def delete_card(current_user, card_id):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    card = Card.query.filter_by(wallet_id=wallet.id, id=card_id).first()

    if not card:
        return jsonify({'message': 'No card found!'})

    db.session.delete(card)
    db.session.commit()
    return jsonify({'message': 'The card has been deleted!'})
