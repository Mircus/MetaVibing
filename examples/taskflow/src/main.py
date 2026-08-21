"""
TaskFlow — the MetaVibing sandbox application.

A deliberately small FastAPI app used throughout the MetaVibing manual as a
reproducible laboratory. It is intentionally imperfect in places so that
readers can watch Claude's operating environment evolve chapter by chapter.

Intentional architectural quirk: database access is mixed into route handlers
below (demonstrated and fixed in Part III of the manual).
"""
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Task, User


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="TaskFlow",
    description="The MetaVibing sandbox application",
    version="0.1.0",
    lifespan=lifespan,
)


# ── Users ────────────────────────────────────────────────────────────────────


@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User, session: Session = Depends(get_session)):
    # Intentional quirk: no validation for duplicate emails
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── Tasks ─────────────────────────────────────────────────────────────────────


@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/", response_model=List[Task])
def list_tasks(
    done: Optional[bool] = None,
    session: Session = Depends(get_session),
):
    # Intentional quirk: no pagination yet (added in baseline task 1)
    query = select(Task)
    if done is not None:
        query = query.where(Task.done == done)
    return session.exec(query).all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
