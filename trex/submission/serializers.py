from rest_framework import serializers
from .models import Submission, SubmissionFile
import os


class SubmissionListSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField(read_only=True)
    files = serializers.SerializerMethodField(read_only=True)

    def get_files(self, submission):
        files = submission.files.all()
        # WARN: hardcoded localhost url, change it later
        return ['http//localhost:8000' + file.file.url for file in files]

    def get_is_overdue(self, submission):
        if submission.assignment.due_date is None:
            return False
        return submission.assignment.due_date < submission.submission_time.date()

    class Meta:
        model = Submission
        fields = (
            "submission_id",
            "submission_time",
            "assignment",
            "student",
            "is_overdue",
            "files",
            "status"
        )
        read_only_fields = (
            "submission_id",
            "submission_time",
            "assignment",
            "student",
            "is_overdue",
            "files",
            "status"
        )


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = "__all__"
        read_only_fields = (
            "submission_file_id",
            "submission",
        )


class SubmissionSerializer(serializers.ModelSerializer):
    submission_files = SubmissionFileSerializer(required=False)

    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = (
            "submission_id",
            "submission_time",
            "assignment",
            "student",
        )

