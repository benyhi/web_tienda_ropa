from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Base, engine, SessionLocal
from flask_login import LoginManager
from models.user import Usuario


app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    session = SessionLocal()
    return session.query(Usuario).get(int(id))


Base.metadata.create_all(engine)

with app.app_context():
    from routes.main import mainbp
    from routes.auth import authbp
    from routes.dashboard import dashbp
    app.register_blueprint(mainbp)
    app.register_blueprint(authbp)
    app.register_blueprint(dashbp)


if __name__ == "__main__":
    app.run(debug=True)