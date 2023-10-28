# Generated by Django 4.2.6 on 2023-10-25 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("classroom", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("enrollment_id", models.AutoField(primary_key=True, serialize=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "classroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enrollments",
                        to="classroom.classroom",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enrollments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Enrollment",
                "verbose_name_plural": "Enrollments",
                "ordering": ("enrollment_id",),
            },
        ),
    ]