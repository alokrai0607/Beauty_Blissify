from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    img = Column("img", String(2048))  
    title = Column("title", String(100), nullable=False)  
    description = Column("description", String(2048))  
    category = Column("category", String(100))  
    price = Column("price", Float(10, 2))  
