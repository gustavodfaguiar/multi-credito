from multi_credit import db
import datetime
from sqlalchemy import not_


class Card(db.Model):

    __tablename__ = 'card'
    __table_args__ = (db.UniqueConstraint("number"),)

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, index=True)
    expiration_date = db.Column(db.Date, nullable=False)
    validity_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    cvv = db.Column(db.String(4), nullable=False)
    limit = db.Column(db.Float(precision=2), nullable=False)
    credit = db.Column(db.Float(precision=2), nullable=False)

    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'),
        nullable=False)
    wallet = db.relationship("Wallet")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'number': self.number,
            'expiration_date': self.expiration_date,
            'validity_date': self.validity_date,
            'name': self.name,
            'cvv': self.cvv,
            'limit': self.limit,
            'credit': self.credit,
            'wallet_id': self.wallet_id
        }

    def pay_card(self, value_pay, today, date_validate):
        if today.day > date_validate.day:
            result = self.pay_with_tax(value_pay)
        else:
            result = self.pay_without_tax(value_pay)

        return result

    def pay_with_tax(self, value_pay):
        debtor_value = (self.credit + value_pay)
        interest = value_pay * 0.10
        return debtor_value + interest

    def pay_without_tax(self, value_pay):
        return self.credit + value_pay

    def sum_cards(self, wallet_id):
        cards = self.query.filter_by(wallet_id=wallet_id)
        return sum(card.limit for card in cards)

    def update_dates(self, date_buy, wallet_id):
        cards = [card.serialize for card in Card.query.order_by(
                Card.validity_date.desc(), Card.credit.asc()).filter_by(
                    wallet_id=wallet_id
                )]

        for card in cards:
            card_update = Card.query.filter_by(id=card['id']).first()
            date_update = str(date_buy.year) + "-" + str(date_buy.month) + "-" + str(card_update.validity_date.day)
            format_validity_date = datetime.datetime.strptime(date_update, "%Y-%m-%d").date()
            card_update.validity_date = format_validity_date
            db.session.commit()

    def best_cards(self, date_buy, best_date_buy, wallet_id):
        best_cards = [card.serialize for card in Card.query.order_by(
            Card.validity_date.desc(), Card.credit.asc()).\
                filter(
                    Card.validity_date.between(date_buy, best_date_buy)
                ).\
                filter(
                    Card.wallet_id == wallet_id
                )
            ]

        for card in best_cards:
            difference = abs((card['validity_date'] - date_buy)).days
            card['days'] = difference + 30

        return best_cards


    def worst_cards(self, date_buy, best_date_buy, wallet_id):
        worst_cards = [card.serialize for card in Card.query.order_by(
            Card.validity_date.asc(), Card.credit.asc()).\
                filter(
                    not_(Card.validity_date.between(date_buy, best_date_buy))
                ).\
                filter(
                    Card.wallet_id == wallet_id
                )
            ]

        for card in worst_cards:
            difference = (card['validity_date'] - date_buy).days
            if difference < 0:
                difference = 30 - abs(difference)

            card['days'] = difference

        return sorted(worst_cards, key=lambda o: o['days'], reverse=True)
