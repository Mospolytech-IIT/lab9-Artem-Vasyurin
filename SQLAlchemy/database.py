from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем подключение к базе данных (например, SQLite)
DATABASE_URL = "sqlite:///./test.db"

# Настроим движок SQLAlchemy для подключения
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создадим базовый класс для моделей
Base = declarative_base()

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
