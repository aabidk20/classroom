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
            "teacher_name",
            "teacher",
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
