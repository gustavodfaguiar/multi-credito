from multi_credit import db


class Wallet(db.Model):

    __tablename__ = 'wallet'
    __table_args__ = (db.UniqueConstraint("user_id"),)

    id = db.Column(db.Integer, primary_key=True)
    max_limit = db.Column(db.Float(precision=2), nullable=False)
    user_limit = db.Column(db.Float(precision=2), nullable=False)
    spent_credit = db.Column(db.Float(precision=2), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'max_limit': self.max_limit,
            'user_limit': self.user_limit,
            'available_credit': self.available_credit,
            'user_id': self.user_id
        }

    @property
    def available_credit(self):
        if self.user_limit > 0:
            value = self.spent_credit - self.user_limit
        else:
            value = self.spent_credit - self.max_limit

        return value

    def create_wallet(self, user_id):
        new_wallet = Wallet(
            max_limit=0,
            user_limit=0,
            spent_credit=0,
            user_id=user_id
        )

        try:
            db.session.add(new_wallet)
            db.session.commit()
            return True
        except:
            return False
