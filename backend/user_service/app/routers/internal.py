from fastapi import APIRouter, HTTPException
from ..db import database

# Se crea el router para las comunicaciones entre microservicios
router = APIRouter(
    prefix="/internal",
    tags=["Internal Communication"]
)

# Se realiza la peticion para obtener un usuario por email del auth service
@router.get("/users/{email}")
def getUserForAuth(email: str):
    user = database.GetUserByEmail(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user