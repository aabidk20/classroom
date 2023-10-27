from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

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
