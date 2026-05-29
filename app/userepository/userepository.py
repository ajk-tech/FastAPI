from app.db.models import User,Item,Cart
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
        
        id=user.id

        token=create_session_token(
            {
                "sub":email,
                "id":id
            }
        )

        return {
            "access_token":token,
            "token_type":"bearer"
        }
    
    async def current_user(self,email):
        val=await self.db.execute(
            select(User).where(User.email==email)
        )
        user=val.scalar()

        if not email:
            raise HTTPException(status_code=200,detail=f"Invalid Token")

        return user
    
    async def patch_user(self,id,name=None,email=None):

        

        val= await self.db.execute(
            select(User).where(User.id==id)
        )
        result=val.scalar()

        if not result:
            raise HTTPException(status_code=200,detail=f"User does not exist")
        
        if result.email==email:
            raise HTTPException(status_code=200,detail="email already exists")

        if email is not None:
            result.email=email
        if name is not None:
            result.name=name

        await self.db.commit()
        await self.db.refresh(result)

        return result
            
    async def update_password(self,id,current_password,password):
        val=await self.db.execute(
            select(User).where(User.id==id)
        )
        user=val.scalar()
        
        if not user:
            raise HTTPException(status_code=200,detail="User not found")
        

        verify=pwd_context.verify(
            current_password,
            user.password
        )
        if not verify:
            raise HTTPException (status_code=200,detail="Wrong password")

        hash_new_password=pwd_context.hash(password)

        user.password=hash_new_password

        await self.db.commit()
        await self.db.refresh(user)

        return {
                "message":"Password Updated Successfully"
            }
    
    async def delete_user(self,id):
        val=await self.db.execute(
            select(User).where(User.id==id)
        )
        user=val.scalar()

        if not user:
            raise HTTPException(status_code=200,detail="User not found")

        await self.db.delete(user)

        await self.db.commit()

        return {
            "message":"User deleted successfully"
        }
    
    async def post_items(id,self,items,price):
        val=await self.db.execute(
            select(User).where(User.id==id)
        )
        user=val.scalar()

        if not user :
            raise HTTPException(status_code=200,detail="Invalid Token")
        

        item=Item(
            items=items,
            price=price
        )

        self.db.add(item)

        await self.db.commit()
        await self.db.refresh(item)

    
    







    
