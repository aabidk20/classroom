# Generated by Django 4.2.6 on 2023-10-29 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("assignment", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("submission_id", models.AutoField(primary_key=True, serialize=False)),
                ("submission_time", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("submitted", "Submitted")],
                        default="draft",
                        max_length=10,
                    ),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="assignment.assignment",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Submission",
                "verbose_name_plural": "Submissions",
                "ordering": ["submission_time"],
            },
        ),
    ]
