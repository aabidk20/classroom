from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from .models import Classroom
from .serializers import (
    ClassroomSerializer,
    ClassroomDetailSerializer,
    StudentClassroomListSerializer,
    TeacherClassroomListSerializer,
)
from trex.user.permissions import (
    IsTeacher,
    IsAdmin,
    IsTeacherOfThisClassroom,
)
from core.utils import response_payload


class ClassroomListView(ListAPIView):
    """
    List all classrooms of the user.
    User must be authenticated to access this view.

    If user is a teacher, list all classrooms created by the teacher.
    If user is a student, list all classrooms enrolled by the student.
    Note that response format is different for teachers and students.

    Searching is allowed on classroom_name, description, teacher__first_name, teacher__last_name
    Ordering is allowed on classroom_name, teacher__first_name, created_on
    Pagination is not supported yet.
    """

    permission_classes = [IsAuthenticated, ]

    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        'classroom_name',
        'description',
        'teacher__first_name',
        'teacher__last_name'
    ]

    ordering_fields = [
        'classroom_name',
        'teacher__first_name',
        'created_on'
    ]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            queryset = Classroom.objects.filter(teacher=user)
        elif user.role == 'student':
            queryset = Classroom.objects.filter(enrollments__student=user)
        elif user.is_superuser:
            queryset = Classroom.objects.all()
        else:
            queryset = Classroom.objects.none()
        return queryset

    def get_serializer(self, *args, **kwargs):
        """
        Override get_serializer to return different serializer based on user role.
        Using student serializer for students and teacher serializer for teachers or admins.
        """
        user = self.request.user
        if user.role == 'teacher' or user.is_superuser:
            return TeacherClassroomListSerializer(*args, **kwargs)
        elif user.role == 'student':
            return StudentClassroomListSerializer(*args, **kwargs)
        else:
            return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # return different response if no classrooms found
        if len(serializer.data) == 0:
            return Response(
                response_payload(
                    success=True,
                    message="No classrooms found",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_payload(
                    success=True,
                    message="Classroom list fetched successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )


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


class ClassroomUpdateView(UpdateAPIView):

    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    # NOTE: Explore lookup_field
    lookup_field = "classroom_id"

    # NOTE: Explore the get_queryset method, can we use it to filter based on the request?

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


class ClassroomDeleteView(DestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    lookup_field = "classroom_id"

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
                    message="Classroom not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

# NOTE: Filtering not added anywhere yet, must add as per get params
