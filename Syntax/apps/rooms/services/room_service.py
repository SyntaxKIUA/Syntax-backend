from django.template.defaultfilters import title

from apps.rooms.models import Room
from apps.rooms.repositories.room_repo import RoomListRepository


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

