from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ссылка на бузу данных
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

# подклбчение к базе данных
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Генерация сессий
SessonLocal = sessionmaker(bind=engine)

# общий класс для моделей(models.py)
Base = declarative_base()

# функция для генерации свзязей к базе данных
def get_db():
    db = SessonLocal()

    try:
        yield db

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()