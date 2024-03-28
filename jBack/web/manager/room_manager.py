from django.db import models
from django.db.models import Q

class RoomQuerySet(models.query.QuerySet):
    def find_by_meeting(self, room_id):
        return self.filter(id=room_id)

class RoomManager(models.Manager):
    def get_queryset(self): 
        return RoomQuerySet(self.model, using=self._db)

    def find_by_meeting(self, room_id):
        return self.get_queryset().find_by_meeting(room_id)