from app.userepository.userepository import UserRepository
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schema.User_schema import Login,SignUp,UserResponse
from jose import JWTError

router=APIRouter()

@router.post("/signup")
async def sign_up(item:SignUp,db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.signup(
        item.name,
        item.email,
        item.password
    )

@router.post("/login")
async def sign_in(item:Login,db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    result =await repo.login(
        item.email,
        item.password
    )
    if result is None:
        raise HTTPException(status_code=200,detail=f"Invalid Token")
    return result