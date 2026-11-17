from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import HotelRoom
from .serializers import HotelRoomSerializer 





class HotelRoomListView(APIView):

    def get(self, request):
        ordering = request.query_params.get("ordering")

        allowed_ordering = [
            "price_per_night",
            "-price_per_night",
            "created_at",
            "-created_at"
        ]

        if ordering in allowed_ordering:
            rooms = HotelRoom.objects.all().order_by(ordering)
        else:
            rooms = HotelRoom.objects.all()

        serializer = HotelRoomSerializer(rooms, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = HotelRoomSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"id": serializer.data["id"]}, status=201)

        

class HotelRoomDetailView(APIView):

    def get(self, request, pk):
            room = get_object_or_404(HotelRoom, pk=pk)
            serializer = HotelRoomSerializer(room)
    
            return Response(serializer.data)

    def delete(self, request, pk):
        room = get_object_or_404(HotelRoom, pk=pk)
        room.delete()

        return Response(
            {"message": "Номер успешно удалён"},
            status=200
        )    
