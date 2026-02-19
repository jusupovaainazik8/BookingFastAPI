from sqladmin import ModelView
from ..database.models import (
    UserProfile, Country, City, Service,
    Hotel, HotelImage, Review, Room,
    RoomImage, Booking
)

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.email]

class CountryAdmin(ModelView, model=Country):
    column_list = "__all__"

class CityAdmin(ModelView, model=City):
    column_list = "__all__"

class ServiceAdmin(ModelView, model=Service):
    column_list = "__all__"

class HotelAdmin(ModelView, model=Hotel):
    column_list = "__all__"

class HotelImageAdmin(ModelView, model=HotelImage):
    column_list = "__all__"

class ReviewAdmin(ModelView, model=Review):
    column_list = "__all__"

class RoomAdmin(ModelView, model=Room):
    column_list = "__all__"

class RoomImageAdmin(ModelView, model=RoomImage):
    column_list = "__all__"

class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"