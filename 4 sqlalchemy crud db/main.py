from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Integer, String, Boolean, Column
from sqlalchemy.orm import sessionmaker, declarative_base, Session

#now make engine + session + base
DATABASE_URL="sqlite:///./todos.db" #location of db file 
engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #check same thread ONLY FOR SQLITE DBS
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base() #base model from which all tables models inherit for db NOT SAME AS PYDANTIC! this is from sqlalchemy

#create the ORM MODEL : this is NOT A PYDANTIC MODEL AND NOT FOR POST GET METHODS ITS FOR DB
#this is basically defining the SCHEMA of the table 'Todo'. its just a blueprint for the table

#ORM Model
class Todo(Base):
    __tablename__="todos"
    id= Column(Integer, primary_key=True, index=True)
    title= Column(String, index=True, nullable=False )
    description= Column(String, nullable=True)
    completed = Column(Boolean, default=False)

#create tables
Base.metadata.create_all(bind=engine)

#Utility fn/ Dependancy    -to create a session
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally: 
        db.close()

#pydantic schemas now - for all cruds
class TodoCreate(BaseModel):
    title: str
    description: Optional[str]=None

class TodoUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]=None
    completed: Optional[bool]=False

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    class Config:
        from_attributes = True              #SUPER IMP   (i.e orm_mode)

#___________________________________________schema work done_________________________________

# All setup and design done, now fastapi app and routes

app=FastAPI()

@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session= Depends(get_db)):  #Depends is keyword
    db_todo=Todo(**todo.model_dump())  #in db we store an entry of type orm model of table so in it we unwind the received pydantic model argument.
    try:
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
    except Exception:
        db.rollback() #to keep the transaction safe and cancel all incase error
        raise
    return db_todo

@app.get("/todos/", response_model=List[TodoResponse])            #? what if i write list instead of List
def read_todos(skip:int =0, limit: int=100, db: Session=Depends(get_db)):
    return db.query(Todo).offset(skip).limit(limit).all()          #?  what if jsut db.query(Todo).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id:int , db: Session=Depends(get_db)):
    fetched_todo= db.query(Todo).filter(Todo.id==todo_id).first()
    if not fetched_todo:
        raise HTTPException(404, "Not found")
    return fetched_todo

@app.patch("/todos/{todo_id}", response_model=TodoUpdate)
def update_todo_partial(todo_id: int, todo_update: TodoUpdate, db: Session=Depends(get_db)):
    fetched_todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not fetched_todo:
        raise HTTPException(404, "Not found")
    update_data=todo_update.model_dump(exclude_unset=True) #this is just a dict. we converted to normal dict here
    for key, value in update_data.items():
        setattr(fetched_todo, key, value)
    try:
        db.commit()
        db.refresh(fetched_todo)
    except Exception:
        db.rollback()
        raise
    return fetched_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session=Depends(get_db)):
    fetched_todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not fetched_todo:
        raise HTTPException(404, "Not found")
    try:
        db.delete(fetched_todo)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return {"message: ": "Todo deleted"}















