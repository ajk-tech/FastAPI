from app.db.models import User
from app.auth.security import pwd_context,create_session_token
from sqlalchemy import select
from fastapi import HTTPException

class UserRepository:
    
    def __init__(self,db):
        self.db=db 

    async def signup(self,name,email,password):

        hashed_password=pwd_context.hash(password) 
        
        user=User(
            name=name,
            email=email,
            password=hashed_password
        )

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return  {
            "message": f"User {user.name} created successfully" 
        }
    
    async def login(self,email,password):
        val=await self.db.execute(
            select(User).where(User.email==email)
        )
        user=val.scalar()

        if not user:
            raise HTTPException(status_code=200,detail=f"Invalid Credentials")

        verify=pwd_context.verify(
            password,
            user.password 
        )

        if not verify:
            raise HTTPException(status_code=200,detail=f"Invalid Credentials")
        
        token=create_session_token(
            {
                "sub":email
            }
        )

        return {
            "access_token":token,
            "token_type":"Bearer"
        }
    
    async def current_user(self,email):
        val=await self.db.execute(
            select(User).where(User.email==email)
        )
        user=val.scalar()

        if not email:
            raise HTTPException(status_code=200,detail=f"Invalid Token")

        return user
    
