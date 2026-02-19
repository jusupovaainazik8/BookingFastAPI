from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import HotelImage
from mysite.database.schema import HotelImageInputSchema, HotelImageOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

hotel_image_router = APIRouter(prefix='/hotel-images',tags=['Hotel Images'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_image_router.post('/', response_model=HotelImageOutSchema)
async def create_hotel_image(hotel_image: HotelImageInputSchema, db: Session = Depends(get_db)):
    hotel_image_db = HotelImage(**hotel_image.dict())
    db.add(hotel_image_db)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db

@hotel_image_router.get('/', response_model=List[HotelImageOutSchema])
async def list_hotel_images(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()

@hotel_image_router.get('/{hotel_image_id}', response_model=HotelImageOutSchema)
async def get_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail="Hotel image not found", status_code=404)
    return hotel_image_db

@hotel_image_router.put('/{hotel_image_id}', response_model=dict)
async def update_hotel_image(hotel_image_id: int, hotel_image: HotelImageInputSchema, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail="Hotel image not found",status_code=404)

    for key, value in hotel_image.dict().items():
        setattr(hotel_image_db, key, value)

    db.commit()
    db.refresh(hotel_image_db)
    return {'message': 'HotelImage был успешно изменен!'}


@hotel_image_router.delete('/{hotel_image_id}', response_model=dict)
async def delete_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail="Hotel image not found",status_code=404)
    db.delete(hotel_image_db)
    db.commit()
    return {'message': 'HotelImage был успешно удален!'}