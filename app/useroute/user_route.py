from app.userepository.userepository import UserRepository
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schema.User_schema import Login,SignUp,UserResponse,PatchUser,PatchPassword,AddItems,GetItems
from jose import JWTError
from app.auth.security import verify_token,verify_id
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth_scheme import Oaauth_schema


router=APIRouter()

@router.post("/signup")
async def sign_up(item:SignUp,
                  db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.signup(
        item.name,
        item.email,
        item.password
    )

@router.post("/login")
async def sign_in(formdata:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    result =await repo.login(
        formdata.username,
        formdata.password
    )
    if result is None:
        raise HTTPException(status_code=200,detail=f"Invalid Token")
    return result

@router.get("/profile",response_model=UserResponse)
async def profile(email:str=Depends(verify_token),
    db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.current_user(email)

@router.patch("/{id}",response_model=UserResponse)
async def patch_user(update:PatchUser,id:int=Depends(verify_id),db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.patch_user (
        id,
        update.name,
        update.email
    )

@router.patch("/password/{id}")
async def patch_password(update_pass:PatchPassword,id:int=Depends(verify_id),db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.update_password(
        id,
        update_pass.current_password,
        update_pass.password
    )

@router.delete("/{id}")
async def delete_user(id:int=Depends(verify_id),db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.delete_user(id)

@router.post("/items",response_model=AddItems)
async def post_items(id:int=Depends(verify_id),db:AsyncSession=Depends(get_db)):
    repo=UserRepository(db)

    return await repo.post_items