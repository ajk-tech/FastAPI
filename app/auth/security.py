from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timezone,timedelta

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