from fastapi import FastAPI
app= FastAPI()

@app.get("/")
def home_route():
    return {"message_key1":"Welcome to home page"}

@app.get("/home2")
def home_route():
    return {"Welcome to home page2"}