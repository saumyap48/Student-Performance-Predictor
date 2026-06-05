from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import crud, schemas, database, security
from ml_model import predictor
from utils import csv_export
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix="/predict", tags=["prediction"])

@router.post("/", response_model=schemas.PredictionHistory)
def predict_performance(
    prediction: schemas.PredictionCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    predicted_score = predictor.predict(
        prediction.study_hours,
        prediction.attendance,
        prediction.previous_score,
        prediction.assignments_completed
    )
    return crud.create_prediction(
        db=db,
        prediction=prediction,
        user_id=current_user.id,
        predicted_score=predicted_score
    )

@router.get("/history", response_model=List[schemas.PredictionHistory])
def get_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    return crud.get_predictions(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/export")
def export_history(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    predictions = crud.get_predictions(db=db, user_id=current_user.id)
    if not predictions:
        raise HTTPException(status_code=404, detail="No history found to export")
    
    csv_data = csv_export.generate_csv(predictions)
    
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=prediction_history_{current_user.username}.csv"}
    )
