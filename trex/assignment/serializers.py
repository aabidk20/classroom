from datetime import date

from rest_framework import serializers
from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            "assignment_id",
            "assignment_name",
            "description",
            "due_date"
            ,
            "score",
            "status",
            "created_on",
        )
        read_only_fields = (
            "assignment_id",
            "created_on",
        )

    def validate_score(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Score cannot be negative or greater than 100.")
        return value

    def validate_due_date(self, value):
        if value is not None and value < date.today():
            raise serializers.ValidationError("Due date cannot be earlier than today.")
        return value


class StudentAssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            "assignment_id",
            "assignment_name",
            "due_date",
        )
        read_only_fields = (
            "assignment_id",
            "assignment_name",
            "due_date",
        )


class TeacherAssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            "assignment_id",
            "assignment_name",
            "due_date",
            "status",
            "created_on",
        )
        read_only_fields = (
            "assignment_id",
            "assignment_name",
            "due_date",
            "status",
            "created_on",
        )


class StudentAssignmentDetailSerializer(serializers.ModelSerializer):
    assigned_date = serializers.SerializerMethodField()

    def get_assigned_date(self, assignment):
        return assignment.created_on.date()

    class Meta:
        model = Assignment
        fields = (
            "assignment_id",
            "assignment_name",
            "description",
            "due_date",
            "score",
            "assigned_date",
        )
        read_only_fields = (
            "assignment_id",
            "assignment_name",
            "description",
            "due_date",
            "score",
            "created_on",
        )


class TeacherAssignmentDetailSerializer(serializers.ModelSerializer):
    # Note: add submission count in the future
    assigned_date = serializers.SerializerMethodField()

    def get_assigned_date(self, assignment):
        return assignment.created_on.date()

    class Meta:
        model = Assignment
        fields = (
            "assignment_id",
            "assignment_name",
            "description",
            "due_date",
            "score",
            "status",
            "assigned_date",
        )
        read_only_fields = (
            "assignment_id",
            "assignment_name",
            "description",
            "due_date",
            "score",
            "status",
            "assigned_date",
        )
