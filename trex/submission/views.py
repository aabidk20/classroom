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
    SubmissionSerializer,
)
from trex.user.permissions import (
    IsTeacher,
    IsAdmin,
    IsTeacherOfThisClassroom,
    IsStudent,
    IsStudentOfThisClassroom,
)
from core.utils import response_payload


@extend_schema(tags=["Submissions"])
class SubmissionListView(ListAPIView):
    pass
