from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    name: str
    race_id: Optional[str] = None
    class_id: Optional[str] = None
    background_id: Optional[str] = None
    level: int = 1

    # Atributos (STR, DEX, CON, INT, WIS, CHA)
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    hp_current: int = 0
    hp_max: int = 0

class Race(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    open5e_id: str = Field(unique=True, index=True)
    name: str
    description: str = ""


class CharacterClass(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    open5e_id: str = Field(unique=True, index=True)
    name: str
    hit_die: int = 8


class Background(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    open5e_id: str = Field(unique=True, index=True)
    name: str
    description: str = ""


class Spell(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    open5e_id: str = Field(unique=True, index=True)
    name: str
    description: str = ""
    level: int = 0


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    open5e_id: str = Field(unique=True, index=True)
    name: str
    description: str = ""
