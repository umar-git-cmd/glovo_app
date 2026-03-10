from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import StoreMenu
from mysite.database.schema import StoreMenuOutSchema, StoreMenuInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_menu_router = APIRouter(prefix='/store/menu', tags=['STORE_MENU'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@store_menu_router.post('/', response_model=StoreMenuOutSchema)
async def create_user(store_menu: StoreMenuInputSchema, db: Session = Depends(get_db)):
    store_menu_db = StoreMenu(**store_menu.dict())
    db.add(store_menu_db)
    db.commit()
    db.refresh(store_menu_db)
    return store_menu_db

@store_menu_router.get('/', response_model=List[StoreMenuOutSchema])
async def list_store_menu(db: Session = Depends(get_db)):
    return db.query(StoreMenu).all()

@store_menu_router.get('/', response_model=StoreMenuOutSchema)
async def list_store_menu(store_menu_id: int, db: Session = Depends(get_db)):
    store_menu_db =  db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not store_menu_db:
        raise HTTPException(status_code=400, detail='storeMenu not found')
    return store_menu_db

@store_menu_router.put('/{store_menu_id}', response_model=dict)
async def update_store_menu(store_menu_id: int, store_menu: StoreMenuInputSchema, db: Session = Depends(get_db)):
    store_menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not store_menu_db:
        raise HTTPException(status_code=400, detail='storeMenu not found')

    for store_menu_key, store_menu_router_value in store_menu.dict().items():
        setattr(store_menu_db, store_menu_key, store_menu_router_value)

        db.commit()
        db.refresh(store_menu_db)
        return {'message': 'Редактирован'}


@store_menu_router.delete('/{store_menu_id}', response_model=dict)
async def list_store_menu(store_menu_id: int, db: Session = Depends(get_db)):
    store_menu_db =  db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not store_menu_db:
        raise HTTPException(status_code=400, detail='storeMenu not found')

    db.delete(store_menu_db)
    db.commit()
    return {'message': 'Delete'}
