from rest_framework import generics, permissions, status
from rest_framework.response import Response
from jBack.web.model import Room, Booking
from jBack.web.serializer.room_serializer import RoomSerializer
from rest_framework.generics import ListCreateAPIView
import pdb
class RoomDetailView(generics.GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        room = self.get_object()
        room.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        serializer = self.get_serializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoomListView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        booking_instance = Booking.objects.create(
            room=instance,
            start_time=instance.start_time,
            end_time=instance.end_time)
        booking_instance.save()



