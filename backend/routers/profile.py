from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import schemas, security

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/", response_model=schemas.User)
def get_user_profile(current_user: schemas.User = Depends(security.get_current_user)):
    return current_user
