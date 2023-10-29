from rest_framework import serializers
from .models import Submission


class SubmissionListSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField(read_only=True)

    def get_is_overdue(self, submission):
        return submission.assignment.due_date < submission.submission_time.date()

    class Meta:
        model = Submission
        fields = (
            "submission_id",
            "submission_time",
            "assignment",
            "student",
            "is_overdue",
        )
        read_only_fields = (
            "submission_id",
            "submission_time",
            "assignment",
            "student",
            "is_overdue",
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = (
            "submission_id",
            "submission_time",
            "assignment",
            "student",
        )

