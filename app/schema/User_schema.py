from pydantic import BaseModel

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