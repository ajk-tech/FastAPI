from fastapi import FastAPI
from app.useroute.user_route import router

app=FastAPI()

app.include_router(
    router,
    prefix="/users",
    tags=["users"]
)