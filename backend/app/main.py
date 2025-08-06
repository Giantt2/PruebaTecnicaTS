from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.db import database
from app.routers import users

app = FastAPI()

# Configuracion de CORS para que no haya bloqueo de peticiones con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Se crea la tabla de usuarios al iniciar la aplicacion
database.CreateTable()

@app.get("/")
def root():
    return {"message": "Api funcionando"}

# Se instancia el router de usuarios
app.include_router(users.router)

