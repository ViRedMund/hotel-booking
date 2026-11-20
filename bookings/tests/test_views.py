
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from hotels.models import HotelRoom
from bookings.models import Booking


class BookingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.room = HotelRoom.objects.create(
            description="Standard room",
            price_per_night=Decimal("3000.00")
        )

        self.booking = Booking.objects.create(
            room=self.room,
            date_from="2026-12-10",
            date_to="2026-12-15"
        )

    def test_create_booking(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "date_from": "2026-12-20",
                "date_to": "2026-12-25",
                "room": self.room.id
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("booking_id", response.data)
        self.assertEqual(response.data["room_id"], self.room.id)

    def test_create_booking_with_invalid_dates(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "date_from": "2026-12-25",
                "date_to": "2026-12-20",
                "room": self.room.id
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_create_booking_with_nonexistent_room(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "date_from": "2026-12-20",
                "date_to": "2026-12-25",
                "room": 99999
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_get_room_bookings(self):
        response = self.client.get(
            f"/api/hotels/{self.room.id}/bookings/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.booking.id
        )

    def test_delete_booking(self):
        response = self.client.delete(
            f"/api/bookings/{self.booking.id}/"
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Booking.objects.filter(id=self.booking.id).exists()
        )

    def test_get_bookings_for_nonexistent_room(self):
        response = self.client.get(
            "/api/hotels/99999/bookings/"
        )

        self.assertEqual(response.status_code, 404)
