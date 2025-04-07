from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.utils.helper import verify_access_token
from fastapi import HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

async def check_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    
    if not payload or not payload["role"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as a valid user")
    
    return {"id": payload["sub"], "email": payload["email"], "role" : payload['role']}