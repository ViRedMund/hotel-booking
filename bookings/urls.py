from django.urls import path 
from .views import BookingCreateView, BookingListView, BookingDetailView

urlpatterns = [
    path("", BookingCreateView.as_view(), name="booking-create"),
    path("<int:pk>/", BookingDetailView.as_view(), name="delete-booking")
]