from django.urls import path
from .views import HotelRoomListView, HotelRoomDetailView
from bookings.views import BookingListView

urlpatterns = [
    path("", HotelRoomListView.as_view(), name="hotel-list"), 
    path("<int:pk>/", HotelRoomDetailView.as_view(), name="hotel-detail"),
    path("<int:room_id>/bookings/", BookingListView.as_view(), name="room-bookings")
]