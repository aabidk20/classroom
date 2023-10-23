from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .models import Classroom
from .serializers import ClassroomSerializer, ClassroomListSerializer
from core.utils import response_payload


class ClassroomListView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomListSerializer


class ClassroomCreateView(CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_payload(
                    success=True,
                    message="Classroom created successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                response_payload(
                    success=False,
                    message="Classroom creation failed",
                    data=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class ClassroomDetailView(RetrieveAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    lookup_field = "classroom_id"

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                response_payload(
                    success=True,
                    message="Classroom retrieved successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                response_payload(
                    success=False,
                    message="Classroom not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )


class ClassroomUpdateView(RetrieveUpdateAPIView):

    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    # NOTE: Explore lookup_field
    lookup_field = "classroom_id"

    # NOTE: Explore the get_queryset method, can we use it to filter based on the request?

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                response_payload(
                    success=True,
                    message="Classroom retrieved successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                response_payload(
                    success=False,
                    message="Classroom not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_payload(
                        success=True,
                        message="Classroom updated successfully",
                        data=serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_payload(
                        success=False,
                        message="Classroom update failed",
                        data=serializer.errors,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Http404:
            return Response(
                response_payload(
                    success=False,
                    message="Classroom not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )


class ClassroomDeleteView(RetrieveDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    lookup_field = "classroom_id"

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                response_payload(
                    success=True,
                    message="Classroom retrieved successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                response_payload(
                    success=False,
                    message="Classroom not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                response_payload(
                    success=True,
                    message="Classroom deleted successfully",
                ),
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                response_payload(
                    success=False,
                    status=status.HTTP_404_NOT_FOUND,
                    message="Classroom not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

# NOTE: Filtering not added anywhere yet, must add as per get params
