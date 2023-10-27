from rest_framework import serializers
from .models import Enrollment


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.classroom_name', read_only=True)

    class Meta:
        model = Enrollment
        fields = (
            "enrollment_id",
            "student",
            "student_name",
            "classroom",
            "classroom_name",
            "date_joined",
        )

        # fields = '__all__'


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = (
            "enrollment_id",
            "student",
            "classroom",
            "date_joined",
        )
        read_only_fields = (
            "enrollment_id",
            "date_joined",
        )

        # fields = '__all__'


class EnrollmentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = (
            "enrollment_id",
            "student",
            "classroom",
            "date_joined",
        )
        read_only_fields = (
            "enrollment_id",
            "student",
            "classroom",
            "date_joined",
        )

        # fields = '__all__'
