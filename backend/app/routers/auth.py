from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta, timezone
from app.db import database
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.oauth2 import authenticateUser, create_access_token

SECRET_KEY = "contrasenacontrasena123"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

# Se inicializa el router
router = APIRouter()

# --- Endpoints ---
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
