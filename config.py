from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SECRET_KEY = "clave_secreta"
SQLALCHEMY_DATABASE_URI = "sqlite:///example2.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()