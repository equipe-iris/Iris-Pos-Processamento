from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import PPROCEDURE_DB_HOST, PPROCEDURE_DB_PORT, PPROCEDURE_DB_USERNAME, PPROCEDURE_DB_PASSWORD, PPROCEDURE_DB_DATABASE

DATABASE_URL = f"postgresql://{PPROCEDURE_DB_USERNAME}:{PPROCEDURE_DB_PASSWORD}@{PPROCEDURE_DB_HOST}:{PPROCEDURE_DB_PORT}/{PPROCEDURE_DB_DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()