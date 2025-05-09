from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class GetRooms(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ...


