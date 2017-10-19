from multi_credit.db import db


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    email = db.Column(db.String(240), nullable=False)
    password = db.Column(db.String(240), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
