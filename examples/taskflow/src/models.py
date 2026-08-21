"""
TaskFlow data models.

Intentional architectural quirks are present in this file — the sandbox project
is a laboratory rat, not a production template. The MetaVibing manual uses
these to demonstrate progressive improvement through meta-code.
"""
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    done: bool = Field(default=False)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # Intentional quirk: no priority field yet (added in ch. 3 experiment)
    # Intentional quirk: no created_at timestamp (added in ch. 5 experiment)
