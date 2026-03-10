from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Product
from mysite.database.schema import ProductOutSchema, ProductInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

product_router = APIRouter(prefix='/product', tags=['PRODUCT'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/', response_model=ProductOutSchema)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get('/', response_model=List[ProductOutSchema])
async def detail_product(db: Session = Depends(get_db)):
    return db.query(Product).all()

@product_router.get('/{product_id}', response_model=ProductOutSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db =  db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=400, detail='product not found')
    return product_db


@product_router.put('/{product_router}', response_model=dict)
async def update_product(product_id: int, product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not Product:
        raise HTTPException(status_code=400, detail='product not found')

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value )

    db.commit()
    db.refresh(product_db)
    return {'message': 'Успешно редактирован'}

@product_router.delete('/{product_id}', response_model=dict)
async def delete_product(user_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == user_id).first()
    if not product_db:
        raise HTTPException(status_code=400, detail='product not found')

    db.delete(product_db)
    db.commit()
    return {'message': 'удален'}
