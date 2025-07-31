from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.users import UserCreate
from src.crud import users as users_crud
from src.db import get_db
router = APIRouter()

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users_crud.verify_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_crud.create_user(db, user)

