from sqlalchemy.orm import Session
from . import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        img=product.img,
        title=product.title,
        description=product.description,
        category=product.category,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id).first()

def update_product(db: Session, id: int, product: schemas.ProductUpdate):

    db_product = get_product(db, id)
    
    if db_product:
        if product.img is not None:
            db_product.img = product.img
        if product.title is not None:
            db_product.title = product.title
        if product.description is not None:
            db_product.description = product.description
        if product.category is not None:
            db_product.category = product.category
        if product.price is not None:
            db_product.price = product.price
            
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, id: int):
    db_product = get_product(db, id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
