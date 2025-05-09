from django.db import models

from apps.users.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        User,
        through='RoomMembership',
        related_name='rooms'
    )


class RoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='room_memberships/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'room')
