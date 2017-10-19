import os
from multi_credit.db import db
from flask import Flask


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'multi_credit.config.DevelopmentConfig'))


with app.app_context():
    db.init_app(app)
