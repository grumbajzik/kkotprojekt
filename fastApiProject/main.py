from fastapi import FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from Controllers import *
from database import engine
from Entities import *  # import všech modelů
from database import Base
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(reservation_router)
app.include_router(equipment_router)


@app.get("/")
async def root():
    a: int = 5
    return {"message": "Hello World", "numer": {str(a)}}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



# @app.post("/users/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username
#     password = form_data.password
#     # ověření uživatele, vytvoření JWT tokenu
#     return {"access_token": "tvuj_token", "token_type": "bearer"}