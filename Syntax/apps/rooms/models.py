from django.core.validators import FileExtensionValidator
from django.db import models

from Config.settings import DEFAULT_ROOM_IMAGE
from apps.Utils.room.valations_file import validate_file_size
from apps.users.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='room_media', default= DEFAULT_ROOM_IMAGE) #change the default image
    members = models.ManyToManyField(
        User,
        through='RoomMembership',
        related_name='rooms',
    )
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.members.count()} members, {self.members.first().username}"


class RoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='room_memberships/', blank=True, null=True,
                                  validators=[
                                      validate_file_size, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])
                                              ]
                                  )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='unique_room_membership'),
        ]
