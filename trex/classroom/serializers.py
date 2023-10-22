from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = (
            "classroom_id",
            "classroom_name",
            "description",
            "classroom_code",
            "teacher_id",
            "created_on",
        )


class ClassroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = (
            "classroom_name",
            "teacher_id", # NOTE:send teacher name instead
        )
