from multi_credit.db import db
from flask import jsonify, Blueprint, request
from multi_credit.wallet.models import Wallet
from multi_credit.card.models import Card
from multi_credit.security import token_required
import datetime
from operator import attrgetter


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


# PUT /wallet/buy
@wallet.route('/v1/wallet/buy', methods=['PUT'])
@token_required
def buy_wallet(current_user):
    value = request.json.get('value')
    date_now = request.json.get('date') if request.json.get('date') else datetime.datetime.now().strftime('%Y-%m-%d')

    wallet = Wallet.query.filter_by(
        user_id=current_user.id).first()

    if wallet.user_limit > 0 and value > wallet.user_limit:
        return jsonify({'message': 'Purchase value greater than the limit reported by the user!'}), 422
    elif value > wallet.max_limit:
        return jsonify({'message': 'Purchase value greater than the limit!'}), 422

    cards = []
    days = 10
    date_buy = datetime.datetime.strptime(date_now, '%Y-%m-%d').date()
    best_date_buy = date_buy + datetime.timedelta(days=days)

    card_buy = Card()
    card_buy.update_dates(date_buy, wallet.id)

    best_cards = card_buy.best_cards(date_buy, best_date_buy, wallet.id)
    worst_cards = card_buy.worst_cards(date_buy, best_date_buy, wallet.id)

    cards = best_cards + worst_cards

    if value <= cards[0]['credit']:
        card = Card.query.filter_by(id=cards[0]['id']).first()
        card.credit = cards[0]['credit'] - value
        try:
            db.session.commit()
        except:
            return jsonify({'message': 'Error when buying'})

        return jsonify({
            'message': {'credit': card.credit, 'number': card.number}
        }), 201
    else:
        list_card_buy = []
        small_value = value
        sum_total = 0
        for card in cards:

            small_value -= card['credit']
            sum_total += card['credit']

            card_update = Card.query.filter_by(id=card['id']).first()
            if small_value <= 0:
                card_update.credit = abs(small_value)
            else:
                card_update.credit = card_update.credit - card['credit']

            try:
                db.session.commit()
                list_card_buy.append({
                    'credit': card_update.credit,
                    'number': card_update.number
                })
            except:
                return jsonify({'message': 'Error when buying'})

            if sum_total >= value:
                break

        return jsonify({'message': list_card_buy}), 201
