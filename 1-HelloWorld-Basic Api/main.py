from fastapi import FastAPI
app= FastAPI()

@app.get("/")
def home_route():
    return {"message_key1":"Welcome to home page"}

@app.get("/home2") #static route
def home_route():
    return {"Welcome to home page2"}

@app.get("/cats/{breed}") #path params used in route
def cats(breed :str):
    return {f"This cat is of breed {breed}"}

@app.get("/kittens/{breed_type}") #query params also added
def cats(breed_type :str, color :str="orange", age: int|None = None):
    return {f"This cat is of breed {breed_type} and color {color}. \n It's age is {age}."}