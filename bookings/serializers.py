from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "date_from", "date_to", "room"]

    def validate(self, attrs):
        date_from = attrs["date_from"]
        date_to = attrs["date_to"]

        if date_from >= date_to:
            raise serializers.ValidationError(
                "Дата окончания должна быть позже даты начала"
            )

        return attrs