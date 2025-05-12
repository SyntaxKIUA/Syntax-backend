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
        return f"{self.name}, {self.members.count()} members"


class RoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='unique_room_membership'),
        ]

    def __str__(self):
        return f"{self.user.username}, {self.room.name}"


class RoomTaskSubmission(models.Model):
    membership = models.ForeignKey(RoomMembership, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(
        upload_to='room_submissions/',
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'zip', 'jpg', 'png']),
        ]
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    is_late = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['submitted_at']),
            models.Index(fields=['membership']),
        ]

    def __str__(self):
        return f"{self.membership.user.username} - {self.title}"