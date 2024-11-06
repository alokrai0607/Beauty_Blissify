from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services, database

router = APIRouter()

@router.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return services.create_product(db=db, product=product)


@router.get("/products/", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(database.get_db)):
    return services.get_products(db=db)


@router.get("/products/{id}", response_model=schemas.ProductResponse)
def read_product(id: int, db: Session = Depends(database.get_db)):
    db_product = services.get_product(db=db, id=id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.patch("/products/{id}", response_model=schemas.ProductResponse)
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    db_product = services.update_product(db=db, id=id, product=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/products/{id}", response_model=schemas.ProductResponse)
def replace_product(id: int, product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return update_product(id, product, db)


@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(database.get_db)):
    db_product = services.delete_product(db=db, id=id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
