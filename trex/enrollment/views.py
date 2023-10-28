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
from rest_framework.views import APIView
from core.utils import response_payload
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from trex.user.permissions import (
    IsTeacher,
    IsAdmin,
    IsTeacherOfThisClassroom,
    IsStudent,
)
from .models import Enrollment
from .serializers import (
    EnrollmentDetailSerializer,
    EnrollmentCreateSerializer,
    EnrollmentDeleteSerializer
)


class EnrollmentListView(ListAPIView):
    """
    List all enrollments in the current classroom.
    User must be authenticated to access this view.
    Only teacher of current classroom can access this view.
    Searching is allowed on student__first_name, student__last_name, student__id, classroom__classroom_name, classroom__classroom_id
    Ordering is allowed on student__first_name, student__last_name, student__id, classroom__classroom_name, classroom__classroom_id, date_joined
    """

    permission_classes = [IsAuthenticated & (IsTeacherOfThisClassroom | IsAdmin), ]
    serializer_class = EnrollmentDetailSerializer
    # lookup_field = "classroom_id"
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        'student__first_name',
        'student__last_name',
        'student__id',
        'classroom__classroom_name',
        'classroom__classroom_id',
    ]

    ordering_fields = [
        'student__first_name',
        'student__last_name',
        'student__id',
        'classroom__classroom_name',
        'classroom__classroom_id',
        'date_joined',
    ]

    def get_queryset(self):
        classroom_id = self.kwargs['classroom_id']
        return Enrollment.objects.filter(classroom_id=classroom_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # handle empty results
        if len(serializer.data) == 0:
            return Response(
                response_payload(
                    success=True,
                    message="No enrollments found",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            response_payload(
                success=True,
                message="Enrollments fetched successfully",
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class EnrollmentCreateView(CreateAPIView):
    """
    Create a new enrollment.

    Only student can enroll in a classroom, using the classroom_code.
    """

    permission_classes = [IsAuthenticated & IsStudent, ]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check if student is already enrolled in this classroom
            classroom_code = serializer.validated_data.get('classroom_code')
            if Enrollment.objects.filter(classroom__classroom_code=classroom_code, student=request.user).exists():
                return Response(
                    response_payload(
                        success=False,
                        message="You are already enrolled in this classroom",
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                response_payload(
                    success=True,
                    message="User enrolled successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                response_payload(
                    success=False,
                    message="User enrollment failed",
                    data=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
