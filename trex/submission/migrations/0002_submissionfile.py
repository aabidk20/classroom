# Generated by Django 4.2.6 on 2023-10-29 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("submission", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubmissionFile",
            fields=[
                (
                    "submission_file_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("file", models.FileField(upload_to="")),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="submission.submission",
                    ),
                ),
            ],
            options={
                "verbose_name": "Submission File",
                "verbose_name_plural": "Submission Files",
                "ordering": ["submission_file_id"],
            },
        ),
    ]