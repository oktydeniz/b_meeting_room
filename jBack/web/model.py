from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from jBack.web.manager.room_manager import RoomManager


class Room(models.Model):
    name = models.CharField(max_length=100)
    max_occupancy = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=100)
    objects = RoomManager()
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "room"
    
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    all_attendees = models.IntegerField(default=0)
    booking_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookings')

    @property
    def number_of_attendees(self):
        return self.booking_users.count()

    def __str__(self):
        return f"{self.room.name} booking from {self.start_time} to {self.end_time}"
    
    class Meta:
        db_table = "booking"
