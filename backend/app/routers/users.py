from fastapi import APIRouter
from pydantic import BaseModel
from app.db import database
import requests


# --- Modelos ---
class User(BaseModel):
    name: str
    email: str
    password: str

# URL de servicio de websocket en Go
WEBSOCKET_SERVICE_URL = "http://127.0.0.1:8081/broadcast"

# Función para enviar la notificación al servicio de Go
def send_broadcast(message: str):
    try:
        response = requests.post(WEBSOCKET_SERVICE_URL, json={"message": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio de WebSocket: {e}")


def get_router():
    router = APIRouter()

    # --- Rutas ---

    # Ruta para crear un usuario
    @router.post("/users")
    async def createUser(user: User):

        try:
            database.InsertUser(user.name, user.email, user.password)

            # Se notifica a traves del websocket que se ha creado un usuario
            send_broadcast(f"Se ha creado un nuevo usuario: {user.name}")
            return {"message": "El usuario se creo correctamente", "user": user}
        except Exception as e:
            return {"error": str(e)}
        
    # Ruta para obtener usuarios
    @router.get("/users")
    def getUsers():
        try:
            users = database.GetUsers()
            return {"users": users}
        except Exception as e:
            return {"error": str(e)}
        
    # Ruta para actualizar un usuario
    @router.put("/users/{id}")
    async def updateUser(id: int, user: User):
        try:
            database.UpdateUser(id, user.name, user.email, user.password)
            send_broadcast(f"✏️ Usuario actualizado: {user.name}")
            return {"message": "Usuario actualizado correctamente"}
        except Exception as e:
            return {"error": str(e)}
        
    # Ruta para eliminar un usuario
    @router.delete("/users/{id}")
    async def deleteUser(id: int):
        try:
            database.DeleteUser(id)
            send_broadcast(f"Usuario eliminado con ID {id}")
            return {"message": "Usuario eliminado correctamente"}
        except Exception as e:
            return {"error": str(e)}

    return router