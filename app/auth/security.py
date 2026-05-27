from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timezone,timedelta
from fastapi import Depends,HTTPException
from app.core.auth_scheme import Oaauth_schema

SECRET_KEY="mysecret123"
ALGORITHM="HS256" 

pwd_context=CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def create_session_token(data:dict):
    
    try:
        to_encode=data.copy()
        expire=datetime.now(timezone.utc)+timedelta(minutes=15)

        to_encode.update(
            {
                "exp":expire
            }
        )

        token = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        
        return token
    
    except JWTError:
        return None
    
def verify_token(token:str=Depends(Oaauth_schema)):
    try:
        result=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email=result.get("sub")

        if not email :
            raise HTTPException(status_code=200,detail="Invalid Token")
        
        return email
    
    except JWTError:
        raise HTTPException(status_code=401)