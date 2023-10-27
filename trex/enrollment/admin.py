from django.contrib import admin
from .models import Enrollment

# Register your models here.
#


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment_id",
        "get_student",
        "get_classroom",
        "date_joined",
    )

    def get_student(self, obj):
        return obj.student.get_full_name()
    get_student.short_description = 'Student Name'

    def get_classroom(self, obj):
        return obj.classroom.classroom_name
    get_classroom.short_description = 'Classroom Name'

    list_filter = (
        "classroom",
        "date_joined",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
        "classroom__classroom_name",
        "classroom__teacher__first_name",
        "classroom__teacher__last_name",
    )

    ordering = (
        "-enrollment_id",
    )

    def has_change_permission(self, request, obj=None):
        return False
