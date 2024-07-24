from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Base, engine, SessionLocal
from flask_login import LoginManager
from models.bd import Usuario


app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    session = SessionLocal()
    return session.query(Usuario).get(int(id))


Base.metadata.create_all(engine)

with app.app_context():
    from routes.main import bp
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True)