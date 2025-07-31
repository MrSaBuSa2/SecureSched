from sqlalchemy.orm import Session
from src.models.users import User
from src.schemas.users import UserCreate, UserUpdate  # à créer si pas encore fait
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_create: UserCreate):
    hashed_password = pwd_context.hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        is_admin=False  # ou True si besoin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.hashed_password = pwd_context.hash(user_update.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
def verify_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user