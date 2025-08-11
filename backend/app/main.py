from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.db import database
from app.routers import users, auth

# Se instancia FastAPI
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

# Se instancian los routers
app.include_router(users.get_router())
app.include_router(auth.router)
