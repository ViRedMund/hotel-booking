from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import BookingSerializer
from .models import Booking
from hotels.models import HotelRoom



class BookingCreateView(APIView):

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "booking_id": serializer.data["id"],
                "room_id": serializer.data["room"]
            },
            status=201
        )



class BookingListView(APIView):
    def get(self, request, room_id):
        room = get_object_or_404(HotelRoom, pk=room_id)
        
        all_room_booking = Booking.objects.filter(room_id=room_id).order_by("date_from")
        serializer = BookingSerializer(all_room_booking, many=True)

        return Response(serializer.data)

class BookingDetailView(APIView):
    def delete(self, request, pk):
            booking = get_object_or_404(Booking, pk=pk)
            booking.delete()
    
            return Response(
                        {"message": "Бронирование успешно удалёно"},
                        status=200
                    )   




