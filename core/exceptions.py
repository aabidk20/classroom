from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.utils import response_payload


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return custom response payload
    """
    if isinstance(exc, PermissionDenied):
        return Response(
            response_payload(
                success=False,
                message="You do not have permission to perform this action",
            ),
            status=status.HTTP_403_FORBIDDEN,
        )

    response = exception_handler(exc, context)

    return response
