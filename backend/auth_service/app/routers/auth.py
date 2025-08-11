from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import oauth2

router = APIRouter()

class Token(object):
    pass

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await oauth2.authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contrasena incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2.createAccessToken(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}