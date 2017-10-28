from multi_credit import app, db


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
    db.create_all(app=app)
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
