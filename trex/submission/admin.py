import os

from django.contrib import admin
from .models import Submission

# Register your models here.


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        "submission_id",
        "submission_time",
        "status",
        "get_assignment_id",
        "assignment",
        "get_student_id",
        "get_student_name",
        "get_submission_files",
    ]

    def get_assignment_id(self, obj):
        return obj.assignment.assignment_id
    get_assignment_id.short_description = 'Assignment ID'

    def get_student_id(self, obj):
        return obj.student.id
    get_student_id.short_description = 'Student ID'

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    get_student_name.short_description = 'Student Name'

    def get_submission_files(self, obj):
        return [os.path.basename(i.file.path)for i in obj.files.all()]
    get_submission_files.short_description = 'Submission Files'
