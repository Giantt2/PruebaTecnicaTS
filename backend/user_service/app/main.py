from fastapi import FastAPI
from .db import database
from .routers import users, internal

app = FastAPI()

database.CreateTable()

app.include_router(users.router)
app.include_router(internal.router)