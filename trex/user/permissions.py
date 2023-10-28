from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.utils import response_payload


class IsAdmin(BasePermission):
    message = response_payload(
        success=False,
        message="Only admins can perform this action",
    )

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsTeacher(BasePermission):
    message = response_payload(
        success=False,
        message="Only teachers can perform this action",
    )

    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class IsTeacherOfThisClassroom(BasePermission):
    message = response_payload(
        success=False,
        message="Only teachers of this classroom can perform this action",
    )

    def has_permission(self, request, view):
        classroom_id = view.kwargs['classroom_id']
        # This works because of the related_name='classrooms' in Classroom model.
        # Only teacher has 'classrooms' attribute, not the students.
        return request.user.classrooms.filter(classroom_id=classroom_id).exists()


class IsStudent(BasePermission):
    message = response_payload(
        success=False,
        message="Only students can perform this action",
    )

    def has_permission(self, request, view):
        return request.user.role == 'student'
