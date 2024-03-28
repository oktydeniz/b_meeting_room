
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from jBack.web.model import Room
from jBack.web.serializer.room_serializer import RoomSerializer
from rest_framework.permissions import AllowAny
from email.utils import parsedate_to_datetime
from django.db.models import Q
from django.db.models import F, ExpressionWrapper, IntegerField, Sum
from django.db.models.functions import Coalesce

@api_view(['GET'])
@permission_classes([AllowAny])
def available_rooms(request):
    number_of_people = int(request.GET.get('max_occupancy', 0))
    start = parsedate_to_datetime(request.GET.get('start_time'))
    end = parsedate_to_datetime(request.GET.get('end_time'))
    if not all([number_of_people, start, end]):
        return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
    available_rooms = Room.objects.annotate(
        available_capacity=F('max_occupancy') - Coalesce(Sum('bookings__all_attendees', filter=Q(bookings__start_time__lt=end, bookings__end_time__gt=start)), 0)
    ).filter(
        available_capacity__gte=number_of_people
    ).filter(
        Q(bookings__start_time__gte=end) | Q(bookings__end_time__lte=start)
    ).distinct()

    serializer = RoomSerializer(available_rooms, many=True)
    return Response(serializer.data)


