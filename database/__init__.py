from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
    )

Base = declarative_base()

from database import models

def get_db():
    db: Session = SessionLocal()
    
    try:
        yield db

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()