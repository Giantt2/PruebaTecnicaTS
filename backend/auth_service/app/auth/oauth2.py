from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import httpx

SECRET_KEY = "contrasena"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360
USER_SERVICE_URL = "http://127.0.0.1:8000"

# Contexto para el hashing de contrasenas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funciones ---

# Funcion para verificar la contrasena
def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Funcion para obtener un usuario por su email
async def GetUserByEmail(email: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USER_SERVICE_URL}/internal/users/{email}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="No se pudo conectar con el servicio de usuarios.")

# Funcion para autenticar un usuario
async def authenticateUser(email: str, password: str):
    user = await GetUserByEmail(email)
    if not user:
        return None
    if not verifyPassword(password, user["password"]):
        return None
    return user

# Funcion para crear un token de acceso
def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)