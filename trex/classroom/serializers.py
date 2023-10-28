import string
from django.utils.crypto import get_random_string
from django.db.models import Q

from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    teacher = serializers.HiddenField(default=serializers.CurrentUserDefault())
    classroom_code = serializers.CharField(read_only=True)

    class Meta:
        model = Classroom
        fields = (
            "classroom_id",
            "classroom_name",
            "description",
            "classroom_code",
            "teacher",
            "teacher_name",
            "created_on",
        )
        # fields = '__all__'

    def create(self, validated_data):
        """
        Create a classroom object, but add the unique classroom_code to the data
        """
        while True:
            classroom_code = get_random_string(length=6, allowed_chars=string.ascii_letters + string.digits)
            if not Classroom.objects.filter(Q(classroom_code=classroom_code)).exists():
                break

        validated_data['classroom_code'] = classroom_code
        return Classroom.objects.create(**validated_data)


class ClassroomDetailSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    student_ids = serializers.SerializerMethodField()

    def get_student_ids(self, classroom):
        student_ids = classroom.enrollments.values_list('student_id', flat=True)
        return student_ids

    class Meta:
        model = Classroom
        fields = (
            "classroom_id",
            "classroom_name",
            "description",
            "classroom_code",
            "teacher",
            "teacher_name",
            "student_ids",
            "created_on",
        )
        # fields = '__all__'


# NOTE: Kept for compatibility with old code for now
class ClassroomListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Classroom
        fields = (
            "classroom_id",
            "classroom_name",
            "teacher_id",
            "teacher_name",
        )


class StudentClassroomListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Classroom
        fields = (
            "classroom_id",
            "classroom_name",
            "teacher_id",
            "teacher_name",
        )


class TeacherClassroomListSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()

    def get_student_count(self, classroom):
        return classroom.enrollments.count()

    class Meta:
        model = Classroom
        fields = (
            "classroom_id",
            "classroom_name",
            "classroom_code",
            "student_count",
            "created_on",
        )
        # fields = '__all__'
