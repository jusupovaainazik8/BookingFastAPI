from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(booking_app: FastAPI):
    # Импортту ушул жерге гана жазабыз!
    # Бул жерде кызарып турса көңүл бурбаңыз, бул айланма импорттон качуунун жолу.
    from .views import (
        UserProfileAdmin, CountryAdmin, CityAdmin, ServiceAdmin,
        HotelAdmin, HotelImageAdmin, ReviewAdmin, RoomAdmin,
        RoomImageAdmin, BookingAdmin
    )

    admin = Admin(booking_app, engine)

    admin.add_view(UserProfileAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(HotelImageAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(RoomImageAdmin)
    admin.add_view(BookingAdmin)