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

from drf_spectacular.utils import extend_schema

from .models import Assignment
from .serializers import (
    AssignmentSerializer,
    StudentAssignmentListSerializer,
    TeacherAssignmentListSerializer,
)
from trex.user.permissions import (
    IsTeacher,
    IsAdmin,
    IsTeacherOfThisClassroom,
    IsStudent,
    IsStudentOfThisClassroom,
)
from core.utils import response_payload


@extend_schema(tags=["Assignments"])
class AssignmentListView(ListAPIView):
    """
    List all assignments of a classroom.
    User must be authenticated.

    Student can only view assignments of classrooms that they have joined.
    Teacher can view assignments of all classrooms that they have created.

    Searching is allowed on ...
    Ordering is allowed on ...
    """

    permission_classes = [IsAuthenticated & (IsTeacherOfThisClassroom | IsStudentOfThisClassroom | IsAdmin), ]

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "assignment_name",
        "description",
    ]

    ordering_fields = [
        "assignment_name",
        "due_date",
        "score",
        "status",
        "created_on",
    ]

    def get_queryset(self):
        classroom_id = self.kwargs.get("classroom_id")
        user = self.request.user
        if user.role == "teacher" or user.is_superuser:
            queryset = Assignment.objects.filter(classroom_id=classroom_id)
        elif user.role == "student":
            queryset = Assignment.objects.filter(classroom_id=classroom_id, status="published")
        else:
            queryset = Assignment.objects.none()
        return queryset

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if user.role == "teacher" or user.is_superuser:
            return TeacherAssignmentListSerializer(*args, **kwargs)
        elif user.role == "student":
            return StudentAssignmentListSerializer(*args, **kwargs)
        else:
            return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        if len(serializer.data) == 0:
            return Response(
                response_payload(
                    success=True,
                    message="No assignments found",
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_payload(
                    success=True,
                    message="Assignments fetched successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )


@extend_schema(tags=["Assignments"])
class AssignmentCreateView(CreateAPIView):
    """
    Create an assignment.
    User must be authenticated and teacher of the classroom.
    """
    permission_classes = [IsAuthenticated & (IsTeacherOfThisClassroom | IsAdmin), ]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def create(self, request, *args, **kwargs):
        classroom_id = self.kwargs.get("classroom_id")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(classroom_id=classroom_id)
            return Response(
                response_payload(
                    success=True,
                    message="Assignment created successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                response_payload(
                    success=False,
                    message="Assignment creation failed",
                    data=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
