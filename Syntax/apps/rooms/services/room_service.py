from django.template.defaultfilters import title

from apps.rooms.models import Room, RoomTaskSubmission
from apps.rooms.repositories.room_repo import RoomListRepository, RoomTaskSubmissionRepository


class RoomListService:
    @staticmethod
    def get_rooms_for_user(user):
        return RoomListRepository.get_rooms_for_user(user)

    @staticmethod
    def post_room_tasks(user, room: Room, file, title: str, description: str = ""):
        try:
            membership = RoomListRepository.get_membership(user, room)
            return RoomListRepository.post_tasks(
                membership= membership,
                file=file,
                title=title,
                description=description
            )
        except Exception as e:
            return e

class RoomTaskService:
    @staticmethod
    def get_room_tasks(room):
        return RoomTaskSubmissionRepository.get_tasks(room)

