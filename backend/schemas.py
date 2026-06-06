from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserResponseWithToken(BaseModel):
    user: User
    access_token: str
    token_type: str

class PredictionBase(BaseModel):
    study_hours: float
    attendance: float
    previous_score: float
    assignments_completed: int

class PredictionCreate(PredictionBase):
    pass

class PredictionHistory(PredictionBase):
    id: int
    user_id: int
    predicted_score: float
    created_at: datetime

    class Config:
        from_attributes = True

