from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from apps.rooms.models import Room, RoomTaskSubmission, RoomMembership


class RoomListRepository:
    @staticmethod
    def get_membership(user, room):
        try:
            return RoomMembership.objects.get(user=user, room=room)
        except RoomMembership.DoesNotExist:
            raise PermissionDenied("User is not a member of this room.")

    @staticmethod
    def get_rooms_for_user(user):
        return Room.objects.filter(members=user).prefetch_related("members")

    @staticmethod
    def post_tasks(membership, file, title: str, description: str = ""):
        try:
            return RoomTaskSubmission.objects.create(
                membership=membership,
                file=file,
                title=title,
                description=description,
            )

        except IntegrityError:
            raise Exception("Submission failed due to a database error.")