from multi_credit.db import db


class User(db.Model):

    __tablename__ = 'user'
    __table_args__ = (db.UniqueConstraint("email"),)

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

    @property
    def name_card(self):
        middle_name = ''
        name = self.name.split(' ')
        first_name, last_name = name[0], name[-1]
        for position in range(1, len(name) - 1):
            middle_name += name[position][0] + ' '

        full_name = first_name + ' ' + middle_name + last_name

        return full_name.upper()
