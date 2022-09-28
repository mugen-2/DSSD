from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    with app.app_context():
        from app.models.user import User
        config_db(app)

def config_db(app):
    @app.before_first_request
    def init_database():
        #se crean rodos los modelos
        db.create_all()

    @app.teardown_request
    def close_session(exeption=None):
        db.session.remove()
