from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()