from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    is_admin: Optional[bool] = False
class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str  # mot de passe brut envoyé à l’inscription
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
