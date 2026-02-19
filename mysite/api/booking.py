from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Booking
from mysite.database.schema import BookingInputSchema, BookingOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

booking_router = APIRouter(prefix='/bookings', tags=['Bookings'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@booking_router.post('/', response_model=BookingOutSchema)
async def create_booking(booking: BookingInputSchema, db: Session = Depends(get_db)):
    booking_db = Booking(**booking.dict())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.get('/', response_model=List[BookingOutSchema])
async def list_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@booking_router.get('/{booking_id}', response_model=BookingOutSchema)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(detail="Booking not found", status_code=404)
    return booking_db

@booking_router.put('/{booking_id}', response_model=dict)
async def update_booking(booking_id: int, booking: BookingInputSchema, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(detail="Booking not found",status_code=404)

    for key, value in booking.dict().items():
        setattr(booking_db, key, value)

    db.commit()
    db.refresh(booking_db)
    return {'message': 'Booking был успешно изменен!'}


@booking_router.delete('/{booking_id}', response_model=dict)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(detail="Booking not found",status_code=404)
    db.delete(booking_db)
    db.commit()
    return {'message': 'Booking был успешно удален!'}