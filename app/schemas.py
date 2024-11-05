from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    img: str
    title: str
    description: str
    category: str
    price: float

class ProductUpdate(BaseModel):
    img: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None 

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
