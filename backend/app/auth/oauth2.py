from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import bcrypt
import sqlite3

SECRET_KEY = "contrasenacontrasena123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Modelos ---
class User(BaseModel):
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str


# Funcion para hashear la contrasena
def getPasswordHash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# --- Funciones de autenticacion ---

# Funcion para obtener usuario a traves de su email
def GetUserByEmail(email):
    con = sqlite3.connect('app/db/users.db')
    cur = con.cursor()
    cur.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    con.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "password": row[3]
        }
    return None

# Funcion para verificar la contrasena
def authenticateUser(email: str, password: str):
    user = GetUserByEmail(email)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return None
    return user

# --- Dependencias ---

# Funcion para crear el token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Funcion para decodificar el token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise Exception(f"Token invalido o expirado: {e}")

# Funcion para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    user = GetUserByEmail(email)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


