from .database import Base
from sqlalchemy import Column,Integer,String
class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=False)
    name=Column(String)
    email=Column(String,unique=True)
    password=Column(String)