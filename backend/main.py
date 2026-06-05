from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

import models, database
from routers import auth, prediction, profile
from ml_model.predictor import train_model

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Student Performance Predictor")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(prediction.router)
app.include_router(profile.router)

# 🔥 ADD THIS (LIVE USERS DEBUG API)
@app.get("/debug/users")
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

# Startup event
@app.on_event("startup")
async def startup_event():
    model_path = os.path.join(os.path.dirname(__file__), "../student_model.pkl")
    if not os.path.exists(model_path):
        print("Training ML model...")
        train_model()

# Root
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Performance Prediction API"}
