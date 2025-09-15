from typing import Dict, Optional
from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from sqlalchemy import create_engine, Integer, String, Boolean, Column
from sqlalchemy.orm import sessionmaker, declarative_base, Session

#now make engine + session + base
DATABASE_URL="sqlite:///./todos.db" #location of db file 
engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #check same thread ONLY FOR SQLITE DBS
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base #base model from which all tables models inherit for db NOT SAME AS PYDANTIC! this is from sqlalchemy

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
        orm_mode = True              #SUPER IMP

# All setup and design done, now fastapi app and routes










