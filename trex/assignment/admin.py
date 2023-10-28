from django.contrib import admin
from .models import Assignment

# Register your models here.


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "assignment_id",
        "assignment_name",
        "classroom_id",
        "get_classroom",
        "created_on",
    )

    def get_classroom(self, obj):
        return obj.classroom.classroom_name
    get_classroom.short_description = 'Classroom Name'
