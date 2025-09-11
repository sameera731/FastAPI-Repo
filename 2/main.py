from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class UserDesign(BaseModel):
    name:str
    email: str
    age: int|None= None # class serves as a design only to be extended upon (blueprint). does not make objects of it.

class UserCreate(UserDesign):
    pass #users objects will be made of this when user gives info to db. same design as blueprint design

class User(BaseModel):
    id:int #id will be added by DB 

#fake db
users_db:Dict[int, User]={} #created an empty dict called users_db of type hint Dict[int, User] . dict typehint syntax imported from typing 
next_id=1

#util fn
def get_next_id():
    global next_id
    uid=next_id
    next_id+=1
    return uid

#Create user root by client side
@app.post("/users/", response_model=User)
def makeuser(user: UserCreate):
    user_id=get_next_id()
    new_user=User(id=user_id, **user.model_dump())
    users_db[user_id]=new_user
    return new_user






