from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import CourierProduct
from mysite.database.schema import CourierProductOutSchema, CourierProductInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

courierProduct_router = APIRouter(prefix='/courier/product', tags=['COURIER_PRODUCT'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@courierProduct_router.post('/', response_model=CourierProductOutSchema)
async def create_courierProduct(courier_product: CourierProductInputSchema, db: Session = Depends(get_db)):
    courier_product_db = CourierProduct(**courier_product.dict())
    db.add(courier_product_db)
    db.commit()
    db.refresh(courier_product_db)
    return courier_product_db

@courierProduct_router.get('/', response_model=List[CourierProductOutSchema])
async def list_courier_product(db: Session = Depends(get_db)):
    return db.query(CourierProduct).all()

@courierProduct_router.get('/{courier_product_id}', response_model=CourierProductOutSchema)
async def detail_courier_product(courier_product_id: int, db:  Session = Depends(get_db)):
    courier_product_db = db.query(CourierProduct).filter(CourierProduct.id == courier_product_id).first()
    if not courier_product_db:
        raise HTTPException(status_code=400, detail='courierProduct not found')
    return courier_product_db

@courierProduct_router.put('/{courier_product_id}', response_model=dict)
async def update_courier_product(courier_product_id: int, courier_product: CourierProductInputSchema, db: Session = Depends(get_db)):
    courier_product_db = db.query(CourierProduct).filter(CourierProduct.id == courier_product_id).first()
    if not courier_product_db:
        raise HTTPException(status_code=400, detail='courier_product not found')

    for courier_product_key, courier_product_value in courier_product.dict().items():
        setattr(courier_product_db, courier_product_key, courier_product_value )

    db.commit()
    db.refresh(courier_product_db)
    return {'message': 'Успешно редактирован'}

@courierProduct_router.delete('/{courier_product_id}', response_model=dict)
async def delete_courier_product(courier_product_id: int, db: Session = Depends(get_db)):
    courier_product_db = db.query(CourierProduct).filter(CourierProduct.id == courier_product_id).first()
    if not courier_product_db:
        raise HTTPException(status_code=400, detail='courier_product not found')

    db.delete(courier_product_db)
    db.commit()
    return {'message': 'удален'}

