from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True #Mapeia do SQLMODEL

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
        
class CharacterCreate(BaseModel):
    name: str
    race_id: Optional[str] = None
    level: int = 1
    
class CharacterResponse(BaseModel):
    id: int
    name: str
    level: int
    sthrength: int
    hp_max: int
    
    class Config:
        from_attributes = True