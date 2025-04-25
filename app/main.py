import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.database import engine
from app.routes import dashboard_route, files_route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
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
    logger.info("Tables created successfully")
    port = os.getenv("PORT")
    logger.info(f"Swagger available at http://localhost:{port}/docs")

app.include_router(dashboard_route.router)
app.include_router(files_route.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
