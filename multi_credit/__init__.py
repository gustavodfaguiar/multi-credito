from decouple import config
from multi_credit.db import db
from flask import Flask
from multi_credit.user.views import user
from multi_credit.wallet.views import wallet
from multi_credit.card.views import card
from multi_credit.admin.views import login


app = Flask(__name__)
app.config.from_object(config('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)

app.register_blueprint(wallet, url_prefix='/api')
app.register_blueprint(user, url_prefix='/api')
app.register_blueprint(card, url_prefix='/api')
app.register_blueprint(login, url_prefix='/api')
