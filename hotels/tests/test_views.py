
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from hotels.models import HotelRoom
from bookings.models import Booking


class HotelRoomAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.room1 = HotelRoom.objects.create(
            description="Standard room",
            price_per_night=Decimal("3000.00")
        )

        self.room2 = HotelRoom.objects.create(
            description="Deluxe room",
            price_per_night=Decimal("5000.00")
        )

    def test_create_room(self):
        response = self.client.post(
            "/api/hotels/",
            {
                "description": "Luxury room",
                "price_per_night": "7500.00"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertTrue(
            HotelRoom.objects.filter(description="Luxury room").exists()
        )

    def test_get_rooms(self):
        response = self.client.get("/api/hotels/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_order_rooms_by_price(self):
        response = self.client.get(
            "/api/hotels/?ordering=price_per_night"
        )

        self.assertEqual(response.status_code, 200)

        prices = [
            Decimal(room["price_per_night"])
            for room in response.data
        ]

        self.assertEqual(
            prices,
            sorted(prices)
        )

    def test_get_room_detail(self):
        response = self.client.get(
            f"/api/hotels/{self.room1.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.room1.id)

    def test_delete_room_with_bookings(self):
        booking = Booking.objects.create(
            room=self.room1,
            date_from="2026-12-10",
            date_to="2026-12-15"
        )

        response = self.client.delete(
            f"/api/hotels/{self.room1.id}/"
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            HotelRoom.objects.filter(id=self.room1.id).exists()
        )

        self.assertFalse(
            Booking.objects.filter(id=booking.id).exists()
        )
