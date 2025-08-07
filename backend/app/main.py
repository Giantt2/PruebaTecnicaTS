from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.db import database
from app.routers import users

# Se instancia FastAPI
app = FastAPI()

class ConnectionManager:
    # Se inicializa una lista para almacenar las conexiones activas de WebSocket
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    # Se agrega la nueva instancia a la lista de conexiones activas
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Se elimina la instancia de la lista de conexiones activas
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Se envía un mensaje a todas las conexiones activas
    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Se instancia el manager de conexiones
manager = ConnectionManager()

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
app.include_router(users.get_router(manager))

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)