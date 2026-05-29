from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=False)
    name=Column(String)
    email=Column(String,unique=True,index=True)
    password=Column(String)
    cart=relationship(
        back_populates="owner",
        cascade="all,delete"
    )

class Item(Base):
    __tablename__="items"

    id=Column(Integer,primary_key=True,index=True)
    items=Column(String,index=True,nullable=False)
    price=Column(Integer,nullable=False)
    
class Cart(Base):
    __tablename__="carts"

    id=Column(Integer,primary_key=True,index=True)
    owner=relationship(
        back_populates="users"
    )
    item_id=Column(Integer,ForeignKey("items.id"))
    price=Column(Integer,ForeignKey("items.price"))
    