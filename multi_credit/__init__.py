import os
from multi_credit.db import db
from flask import Flask
from multi_credit.user.views import user
from multi_credit.admin.views import login


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'multi_credit.config.DevelopmentConfig'))

app.register_blueprint(user, url_prefix='/api')
app.register_blueprint(login, url_prefix='/api')

with app.app_context():
    db.init_app(app)
