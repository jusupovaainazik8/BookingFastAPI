from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import RoleChoices, RoomTypeChoices, RoomStatusChoices
from datetime import date, datetime



class CountryInputSchema(BaseModel):
    country_image: str
    country_name: str


class CountryOutSchema(BaseModel):
    id: int
    country_image: str
    country_name: str


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    user_image: Optional[str]
    country_id: Optional[int]
    phone_number: Optional[str]
    user_role: RoleChoices


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    user_image: Optional[str]
    country_id: Optional[int]
    phone_number: Optional[str]
    user_role: RoleChoices
    registered_date: datetime


class UserLoginSchema(BaseModel):
    username: str
    password: str


class CityInputSchema(BaseModel):
    country_id: Optional[int]
    city_image: str
    city_name: str


class CityOutSchema(BaseModel):
    id: int
    country_id: Optional[int]
    city_image: str
    city_name: str


class ServiceInputSchema(BaseModel):
    service_image: str
    service_name: str
    hotel_id: Optional[int]


class ServiceOutSchema(BaseModel):
    id: int
    service_image: str
    service_name: str
    hotel_id: Optional[int]


class HotelInputSchema(BaseModel):
    hotel_name: str
    country_id: int
    city_id: int
    street: str
    postal_code: int
    hotel_stars: int
    description: str
    owner_id: Optional[int]


class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    country_id: int
    city_id: int
    street: str
    postal_code: int
    hotel_stars: int
    description: str
    owner_id: Optional[int]


class HotelImageInputSchema(BaseModel):
    hotel_id: int
    hotel_image: str


class HotelImageOutSchema(BaseModel):
    id: int
    hotel_id: int
    hotel_image: str


class RoomInputSchema(BaseModel):
    hotel_id: int
    room_number: int
    price: int
    room_type: RoomTypeChoices
    room_status: RoomStatusChoices
    description: str


class RoomOutSchema(BaseModel):
    id: int
    hotel_id: int
    room_number: int
    price: int
    room_type: RoomTypeChoices
    room_status: RoomStatusChoices
    description: str


class RoomImageInputSchema(BaseModel):
    room_id: int
    room_image: str


class RoomImageOutSchema(BaseModel):
    id: int
    room_id: int
    room_image: str


class ReviewInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    rating: int
    comment: str


class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    rating: int
    comment: str
    created_date: datetime


class BookingInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date


class BookingOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date
    created_date: datetime