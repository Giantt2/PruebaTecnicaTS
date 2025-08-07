from fastapi import APIRouter
from pydantic import BaseModel
from app.db import database


# Se crea una clase con los atributos de un usuario
class User(BaseModel):
    name: str
    email: str
    password: str

def get_router(manager):
    router = APIRouter()

    # Ruta para crear un usuario
    @router.post("/users")
    async def createUser(user: User):

        try:
            database.InsertUser(user.name, user.email, user.password)

            # Se notifica a traves del websocket que se ha creado un usuario
            await manager.broadcast(f"Se ha creado un nuevo usuario: {user.name}")
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
    def updateUser(id: int, user: User):
        try:
            database.UpdateUser(id, user.name, user.email, user.password)
            return {"message": "Usuario actualizado correctamente"}
        except Exception as e:
            return {"error": str(e)}
        
    # Ruta para eliminar un usuario
    @router.delete("/users/{id}")
    def deleteUser(id: int):
        try:
            database.DeleteUser(id)
            return {"message": "Usuario eliminado correctamente"}
        except Exception as e:
            return {"error": str(e)}

    return router