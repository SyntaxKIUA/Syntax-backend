from apps.rooms.models import Room

class RoomListRepository:
    @staticmethod
    def get_rooms_for_user(user):
        return Room.objects.filter(members=user).prefetch_related("members")