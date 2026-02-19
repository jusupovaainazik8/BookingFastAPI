from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import RoomImage
from mysite.database.schema import RoomImageInputSchema, RoomImageOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

room_image_router = APIRouter(prefix='/room-images', tags=['Room Images'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@room_image_router.post('/', response_model=RoomImageOutSchema)
async def create_room_image(room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
    room_image_db = RoomImage(**room_image.dict())
    db.add(room_image_db)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db

@room_image_router.get('/', response_model=List[RoomImageOutSchema])
async def list_room_images(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()

@room_image_router.get('/{room_image_id}', response_model=RoomImageOutSchema)
async def get_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail="Room image not found", status_code=404)
    return room_image_db

@room_image_router.put('/{room_image_id}', response_model=dict)
async def update_room_image(room_image_id: int, room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail="Room image not found",status_code=404)

    for key, value in room_image.dict().items():
        setattr(room_image_db, key, value)

    db.commit()
    db.refresh(room_image_db)
    return {'message': 'RoomImage был успешно изменен!'}


@room_image_router.delete('/{room_image_id}', response_model=dict)
async def delete_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail="Room image not found",status_code=404)
    db.delete(room_image_db)
    db.commit()
    return {'message': 'RoomImage был успешно удален!'}