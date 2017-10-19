from multi_credit import db


class Wallet(db.Model):

    __tablename__ = 'wallet'
    __table_args__ = (db.UniqueConstraint("user_id"),)

    id = db.Column(db.Integer, primary_key=True)
    max_limit = db.Column(db.Float(), nullable=False)
    user_limit = db.Column(db.Float(), nullable=False)
    credit = db.Column(db.Float(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'max_limit': self.max_limit,
            'user_limit': self.user_limit,
            'credit': self.credit,
            'user_id': self.user_id
        }
