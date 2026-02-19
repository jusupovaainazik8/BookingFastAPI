from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Hotel
from mysite.database.schema import HotelInputSchema, HotelOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
hotel_router = APIRouter(prefix='/hotels', tags=['Hotels'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_router.post('/', response_model=HotelOutSchema)
async def create_hotel(hotel: HotelInputSchema, db: Session = Depends(get_db)):
    hotel_db = Hotel(**hotel.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.get('/', response_model=List[HotelOutSchema])
async def list_hotels(db: Session = Depends(get_db)):
    return db.query(Hotel).all()

@hotel_router.get('/{hotel_id}', response_model=HotelOutSchema)
async def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(detail="Hotel not found", status_code=404)
    return hotel_db

@hotel_router.put('/{hotel_id}', response_model=dict)
async def update_hotel(hotel_id: int, hotel: HotelInputSchema, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(detail="Hotel not found",status_code=404)

    for hotel_key, hotel_value in hotel.dict().items():
        setattr(hotel_db, hotel_key, hotel_value)

    db.commit()
    db.refresh(hotel_db)
    return {'message': 'Hotel был успешно изменен!'}


@hotel_router.delete('/{hotel_id}', response_model=dict)
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(detail="Hotel not found",status_code=404)
    db.delete(hotel_db)
    db.commit()
    return {'message': 'Hotel был успешно удален!'}