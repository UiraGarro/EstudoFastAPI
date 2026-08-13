from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: str

    class Config:
        from_attributes = True #Mapeia do SQLMODEL
        
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