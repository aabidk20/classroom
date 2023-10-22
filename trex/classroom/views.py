from django.shortcuts import render

# Create your views here.

from .models import Classroom
from .serializers import ClassroomSerializer, ClassroomListSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)

from rest_framework.permissions import IsAuthenticated


class ClassroomListView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomListSerializer


class ClassroomCreateView(CreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
