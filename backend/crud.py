from sqlalchemy.orm import Session
import models, schemas, security

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_predictions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.PredictionHistory)\
             .filter(models.PredictionHistory.user_id == user_id)\
             .order_by(models.PredictionHistory.created_at.desc())\
             .offset(skip).limit(limit).all()

def create_prediction(db: Session, prediction: schemas.PredictionCreate, user_id: int, predicted_score: float):
    db_prediction = models.PredictionHistory(
        **prediction.dict(),
        user_id=user_id,
        predicted_score=predicted_score
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
