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

#fns
def hash_Password(password: str)->str:
    return pwd_context.hash(password)

def verify_Password(plain_password: str, hashed_password)->bool:
    return pwd_context.verify(plain_password, hashed_password)

#signup route
@app.post("/signup/")
def signup(user: UserSignup):
    if user.username in users_db:
        raise HTTPException(400,"username already exists")
    hashed_pw=hash_Password(user.password)
    new_user=UserLoginStore(username=user.username, hashed_password=hashed_pw)
    users_db[user.username]=new_user
    return {"message": "User created successfully"}

#login route
@app.post("/login/")
def login(user:UserSignup):
    db_user=users_db.get(user.username)
    if not db_user:
        raise HTTPException(401, "Invalid username or password.")
    if not verify_Password(user.password,db_user.hashed_password):
        raise HTTPException(401, "Password incorrect. Enter again")
    return {"message: ": f"Login successful\n Welcome back {user.username}"}







