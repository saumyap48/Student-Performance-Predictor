from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models, database
from routers import auth, prediction, profile
from ml_model.predictor import train_model
import os

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Student Performance Predictor")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-student-performance-predictor.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(prediction.router)
app.include_router(profile.router)

@app.on_event("startup")
async def startup_event():
    model_path = os.path.join(os.path.dirname(__file__), "../student_model.pkl")
    if not os.path.exists(model_path):
        print("Training ML model...")
        train_model()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Student Performance Prediction API"
    }
