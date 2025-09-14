from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib import CryptContext
from typing import Dict

app= FastAPI()

# superrrrr imp line (to store context of our pwd hashing method in an identifier)
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")                              #IMPPPPPPPPP

#then make models for signup and storing(2)
class UserSignup(BaseModel):
    username: str
    password:str #model that user gives data in while signing up

class UserLoginStore(BaseModel):
    username: str
    hashed_password: str #model stored in db afte hashing pwd


users_db: Dict[str, UserLoginStore]={} #fake db
#cant just do users_db: Dict[UserLoginStore]={} cause dict type hint needs type of keys the values so both for mapping!

#now we will make two fns(that we will need and use in signup and login POST routes) for signup (pwd hashing) and login(pwd verify) by using
#inbuilt methods of passlib bcrypt for pwd hashing and verify

@app.post("/signup/")
def signup(usermodel: UserSignup):
    pass



