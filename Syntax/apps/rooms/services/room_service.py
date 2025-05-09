from apps.rooms.repositories.room_repo import RoomListRepository


class RoomListService:
    @staticmethod
    def get_rooms_for_user(user):
        return RoomListRepository.get_rooms_for_user(user)



