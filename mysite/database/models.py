from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'


class RoomTypeChoices(str, PyEnum):
    luxury = 'Люкс'
    semi_luxury = 'Полулюкс'
    family = 'Семейный'
    economy = 'Эконом'
    single = 'Одноместный'


class RoomStatusChoices(str, PyEnum):
    occupied = 'Занят'
    booked = 'Забронирован'
    available = 'Свободен'


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_image: Mapped[str] = mapped_column(String)
    country_name: Mapped[str] = mapped_column(String(30), unique=True)

    cities: Mapped[List['City']] = relationship(back_populates='country', cascade='all, delete-orphan')
    hotels: Mapped[List['Hotel']] = relationship(back_populates='country', cascade='all, delete-orphan')
    users: Mapped[List['UserProfile']] = relationship(back_populates='country', cascade='all, delete-orphan')




class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey('country.id'), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices, create_constraint=False),
                                                   default=RoleChoices.client)
    registered_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    country: Mapped[Optional['Country']] = relationship(back_populates='users')
    reviews: Mapped[List['Review']] = relationship(back_populates='user', cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship(back_populates='user', cascade='all, delete-orphan')
    owned_hotels: Mapped[List['Hotel']] = relationship(back_populates='owner', cascade='all, delete-orphan')
    tokens: Mapped[List['RefreshToken']] = relationship(back_populates='token_user', cascade='all, delete-orphan')

class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='tokens')
    token: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey('country.id'), nullable=True)
    city_image: Mapped[str] = mapped_column(String)
    city_name: Mapped[str] = mapped_column(String(100))

    country: Mapped[Optional['Country']] = relationship(back_populates='cities')
    hotels: Mapped[List['Hotel']] = relationship(back_populates='city', cascade='all, delete-orphan')


class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_image: Mapped[str] = mapped_column(String)
    service_name: Mapped[str] = mapped_column(String(100))
    hotel_id: Mapped[Optional[int]] = mapped_column(ForeignKey('hotel.id'), nullable=True)

    hotel: Mapped[Optional['Hotel']] = relationship(back_populates='hotel_services')


class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    street: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[int] = mapped_column(Integer)
    hotel_stars: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_profile.id'), nullable=True)

    country: Mapped['Country'] = relationship(back_populates='hotels')
    city: Mapped['City'] = relationship(back_populates='hotels')
    owner: Mapped[Optional['UserProfile']] = relationship(back_populates='owned_hotels')
    hotel_services: Mapped[List['Service']] = relationship(back_populates='hotel', cascade='all, delete-orphan')
    hotel_images: Mapped[List['HotelImage']] = relationship(back_populates='hotel', cascade='all, delete-orphan')
    hotel_rooms: Mapped[List['Room']] = relationship(back_populates='hotel', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='hotel', cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship(back_populates='hotel', cascade='all, delete-orphan')


class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_image: Mapped[str] = mapped_column(String)

    hotel: Mapped['Hotel'] = relationship(back_populates='hotel_images')


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_number: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    room_type: Mapped[RoomTypeChoices] = mapped_column(Enum(RoomTypeChoices, create_constraint=False))
    room_status: Mapped[RoomStatusChoices] = mapped_column(Enum(RoomStatusChoices, create_constraint=False))
    description: Mapped[str] = mapped_column(Text)

    hotel: Mapped['Hotel'] = relationship(back_populates='hotel_rooms')
    room_images: Mapped[List['RoomImage']] = relationship(back_populates='room', cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship(back_populates='room', cascade='all, delete-orphan')


class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room_image: Mapped[str] = mapped_column(String)

    room: Mapped['Room'] = relationship(back_populates='room_images')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped['UserProfile'] = relationship(back_populates='reviews')
    hotel: Mapped['Hotel'] = relationship(back_populates='reviews')


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped['UserProfile'] = relationship(back_populates='bookings')
    hotel: Mapped['Hotel'] = relationship(back_populates='bookings')
    room: Mapped['Room'] = relationship(back_populates='bookings')