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

from .models import Submission
from .serializers import (
    SubmissionListSerializer,
    SubmissionSerializer, SubmissionFileSerializer
)
from trex.user.permissions import (
    IsTeacher,
    IsAdmin,
    IsTeacherOfThisClassroom,
    IsStudent,
    IsStudentOfThisClassroom,
)
from core.utils import response_payload
from trex.assignment.models import Assignment


@extend_schema(tags=["Submissions"])
class SubmissionListView(ListAPIView):
    """
    List all submissions of an assignment.
    Teachers can view all submitted submissions of an assignment.
    Students can view their own submissions of an assignment.

    Searching is allowed on student's first name and last name.
    Ordering is allowed on submission_time, student__first_name and student__last_name.
    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = SubmissionListSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
    ]

    ordering_fields = [
        "submission_time",
        "student__first_name",
        "student__last_name",
    ]

    def get_queryset(self):
        user = self.request.user
        assignment_id = self.kwargs.get("assignment_id")
        if user.role == "teacher":
            queryset = Submission.objects.filter(assignment__assignment_id=assignment_id, status="submitted")
        elif user.role == "student":
            queryset = Submission.objects.filter(assignment__assignment_id=assignment_id, student=user)
        else:
            queryset = Submission.objects.none()
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            assignment_id = self.kwargs.get("assignment_id")
            classroom_id = self.kwargs.get("classroom_id")

            # check if assignment exists and belongs to the classroom
            assignment = Assignment.objects.get(assignment_id=assignment_id, classroom_id=classroom_id)
        except:
            return Response(
                response_payload(
                    success=False,
                    message="Assignment not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # check if there are any submissions
        if len(serializer.data) == 0:
            return Response(
                response_payload(
                    success=True,
                    message="No submissions found",
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_payload(
                    success=True,
                    message="Submissions fetched successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )


@extend_schema(tags=["Submissions"])
class SubmissionCreateView(CreateAPIView):
    """
    Create a submission for an assignment.
    Only student of the classroom can create submission.
    """

    permission_classes = [IsAuthenticated & (IsStudentOfThisClassroom | IsAdmin), ]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get("assignment_id")
        classroom_id = self.kwargs.get("classroom_id")
        user = self.request.user

        # check if assignment exists and belongs to the classroom and is published
        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id,
                                                classroom_id=classroom_id,
                                                status="published")

        except:
            return Response(
                response_payload(
                    success=False,
                    message="Assignment not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if submission already exists
        submission, created = Submission.objects.get_or_create(assignment=assignment, student=user)
        if not created and submission.status == "submitted":
            return Response(
                response_payload(
                    success=False,
                    message="You have already submitted this assignment",
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        if submission.status == "draft":
            serializer = self.get_serializer(submission, data=request.data, partial=True)
            if serializer.is_valid():
                submission = serializer.save(submission=submission)
        serializer = SubmissionFileSerializer(data=request.data)
        if serializer.is_valid():
            # there might be a SubmissionFile record without file, so we need to delete it
            serializer.save(submission=submission)
            submission.files.filter(file="").delete()
            return Response(
                response_payload(
                    success=True,
                    message="Assignment submitted successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                response_payload(
                    success=False,
                    message="Submission failed",
                    data=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


# WARN: this view is not used anywhere for now, create view also handles update
@extend_schema(tags=["Submissions"])
class SubmissionUpdateView(UpdateAPIView):
    """
    Update a submission.
    Only student of the classroom can update submission.
    Submissions can be updated any time, but they will be marked as late if the due date has passed.
    """

    permission_classes = [IsAuthenticated & (IsStudentOfThisClassroom | IsAdmin), ]
    serializer_class = SubmissionSerializer
    lookup_field = "submission_id"

    def get_queryset(self):
        assignment_id = self.kwargs.get("assignment_id")
        submission_id = self.kwargs.get("submission_id")
        queryset = Submission.objects.filter(assignment_id=assignment_id, submission_id=submission_id)
        return queryset

    def update(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get("assignment_id")
        submission_id = self.kwargs.get("submission_id")
        user = self.request.user

        # check if assignment exists and belongs to the classroom and is published
        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id,
                                                status="published")

        except:
            return Response(
                response_payload(
                    success=False,
                    message="Assignment not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if submission exists
        try:
            submission = Submission.objects.get(assignment=assignment, submission_id=submission_id, student=user)
        except:
            return Response(
                response_payload(
                    success=False,
                    message="Submission not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # update a submission
        serializer = self.get_serializer(submission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_payload(
                    success=True,
                    message="Submission updated successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_payload(
                    success=False,
                    message="Assignment update failed",
                    data=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(tags=["Submissions"])
class SubmissionDeleteView(DestroyAPIView):
    """
    Delete a submission.
    Only students who have submitted the assignment can delete their submission.
    """

    permission_classes = [IsAuthenticated & (IsStudentOfThisClassroom | IsAdmin), ]
    lookup_field = "submission_id"

    def get_queryset(self):
        assignment_id = self.kwargs.get("assignment_id")
        queryset = Submission.objects.filter(assignment_id=assignment_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get("assignment_id")
        submission_id = self.kwargs.get("submission_id")

        # check if assignment exists and belongs to the classroom and is published
        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id,
                                                status="published")

        except:
            return Response(
                response_payload(
                    success=False,
                    message="Assignment not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if submission exists
        try:
            submission = Submission.objects.get(assignment=assignment, submission_id=submission_id)
        except:
            return Response(
                response_payload(
                    success=False,
                    message="Submission not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # delete a submission
        submission.delete()
        return Response(
            response_payload(
                success=True,
                message="Submission deleted successfully",
            ),
            status=status.HTTP_200_OK,
        )
