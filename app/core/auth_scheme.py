from fastapi.security import OAuth2PasswordBearer

Oaauth_schema=OAuth2PasswordBearer(
    tokenUrl="/users/login"
)