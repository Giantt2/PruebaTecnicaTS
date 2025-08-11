from fastapi import APIRouter, Depends
from pydantic import BaseModel
import requests
from ..db import database
from ..auth import oauth2

# --- Modelos ---
class User(BaseModel):
    name: str
    email: str
    password: str

# Se define el prefijo para todas las rutas de esta clase
router = APIRouter(prefix="/users", tags=["Users"])

# URL de servicio de websocket en Go
WEBSOCKET_SERVICE_URL = "http://127.0.0.1:8081/broadcast"

# Función para enviar la notificación al servicio de Go
def sendBroadcast(message: str):
    try:
        response = requests.post(WEBSOCKET_SERVICE_URL, json={"message": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio de WebSocket: {e}")

# --- Rutas ---

# Ruta para crear un usuario
@router.post("")
def createUser(user: User):
    try:
        database.InsertUser(user.name, user.email, user.password)
        # Se notifica a traves del websocket que se ha creado un usuario
        sendBroadcast(f"Se ha creado un nuevo usuario: {user.name}")
        return {"message": "El usuario se creo correctamente", "user": user}
    except Exception as e:
        return {"error": str(e)}

# Ruta para obtener usuarios
@router.get("")
def getUsers(current_user: dict = Depends(oauth2.getCurrentUser)):
    try:
        users = database.GetUsers()
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}

# Ruta para actualizar un usuario
@router.put("/{id}")
def updateUser(id: int, user: User, current_user: dict = Depends(oauth2.getCurrentUser)):
    try:
        database.UpdateUser(id, user.name, user.email, user.password)
        sendBroadcast(f"Usuario actualizado: {user.name}")
        return {"message": "Usuario actualizado correctamente"}
    except Exception as e:
        return {"error": str(e)}

# Ruta para eliminar un usuario
@router.delete("/{id}")
def deleteUser(id: int, current_user: dict = Depends(oauth2.getCurrentUser)):
    try:
        database.DeleteUser(id)
        sendBroadcast(f"Usuario eliminado con ID {id}")
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        return {"error": str(e)}