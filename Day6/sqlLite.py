from typing import Optional, List
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select


DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL, echo=True)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="To-Do API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/task", response_model=Task)
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks", response_model=List[Task])
def read_tasks():
    with Session(engine) as session:
        statement = select(Task)
        tasks = session.exec(statement).all()
        return tasks
