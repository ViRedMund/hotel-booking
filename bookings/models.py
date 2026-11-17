from django.db import models
from hotels.models import HotelRoom

# Create your models here.
class Booking(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name="bookings")
    