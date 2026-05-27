from pydantic import BaseModel
from typing import Optional

class SignUp(BaseModel):
    name:str
    email:str
    password:str

class Login(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

class PatchUser(BaseModel):
    name:Optional[str]=None
    email:Optional[str]=None
    
class PatchPassword(BaseModel):
    current_password:str
    password:str