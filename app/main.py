import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.database import engine, SessionLocal
from app.routes import dashboard_route, files_route, tickets_route, settings_route
from app.utils.settings_utils import ensure_settings_exists

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

allowed_origins = os.getenv("PPROCEDURE_ALLOWED_ORIGINS", "")
origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        ensure_settings_exists(db)
    except Exception as e:
        logger.error(f"Error ensuring settings exist: {e}")
        db.rollback()
    finally:
        db.close()

    logger.info("Tables created successfully")
    port = os.getenv("PPROCEDURE_PORT")
    logger.info(f"Swagger available at http://localhost:{port}/docs")

app.include_router(dashboard_route.router)
app.include_router(files_route.router)
app.include_router(tickets_route.router)
app.include_router(settings_route.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
