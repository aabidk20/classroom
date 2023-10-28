from django.db.models import Q
from rest_framework import serializers
from .models import Enrollment
from trex.classroom.models import Classroom


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
    classroom_code = serializers.CharField(write_only=True)
    classroom_name = serializers.CharField(source='classroom.classroom_name', read_only=True)

    class Meta:
        model = Enrollment
        fields = (
            "enrollment_id",
            "classroom_id",
            "classroom_name",
            "classroom_code",
            "date_joined",
        )
        read_only_fields = (
            "enrollment_id",
            "classroom_id",
            "classroom_name",
            "date_joined",
        )

        # fields = '__all__'

    def validate(self, attrs):
        classroom_code = attrs.get('classroom_code')
        # check if classroom_code is valid
        if not Classroom.objects.filter(Q(classroom_code=classroom_code)).exists():
            raise serializers.ValidationError(
                detail="Invalid classroom code",
            )
        return attrs

    def create(self, validated_data):
        classroom_code = validated_data.get('classroom_code')
        classroom = Classroom.objects.get(classroom_code=classroom_code)
        student = self.context.get('request').user
        enrollment = Enrollment.objects.create(
            student=student,
            classroom=classroom,
        )
        return enrollment


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
