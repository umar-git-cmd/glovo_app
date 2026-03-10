from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Category
from mysite.database.schema import CategoryOutSchema, CategoryInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

category_router = APIRouter(prefix='/category', tags=['CATEGORY'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@category_router.post('/', response_model=CategoryOutSchema)
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.get('/', response_model=List[CategoryOutSchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()

@category_router.get('/{category_id}', response_model=CategoryOutSchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=400, detail='category not found')
    return category_db


@category_router.put('/{category_id}', response_model=dict)
async def update_category(category_id: int, category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=400, detail='category not found')

    for category_key, category_value in category.dict().items():
        setattr(category_db, category_key, category_value )

    db.commit()
    db.refresh(category_db)
    return {'message': 'Успешно редактирован'}

@category_router.delete('/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=400, detail='category not found')

    db.delete(category_db)
    db.commit()
    return {'message': 'удален'}
