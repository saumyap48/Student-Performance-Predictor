import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =========================
# DATABASE URL (Render / Local)
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

# fallback for local development
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./student_predictor.db"

# =========================
# ENGINE SETUP
# =========================
connect_args = {}

# SQLite special case
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# =========================
# SESSION
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# BASE MODEL
# =========================
Base = declarative_base()

# =========================
# DB DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
