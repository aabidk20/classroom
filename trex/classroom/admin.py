from django.contrib import admin
from .models import Classroom

# Register your models here.


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        "classroom_id",
        "classroom_name",
        "description",
        "classroom_code",
        "teacher_id",
        "created_on",
    )
