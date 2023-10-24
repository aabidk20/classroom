# Generated by Django 4.2.6 on 2023-10-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("male", "Male"),
                    ("female", "Female"),
                    ("other", "Other"),
                    ("not-specified", "Not Specified"),
                ],
                default="not-specified",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("teacher", "Teacher"),
                    ("student", "Student"),
                    ("not-specified", "Not Specified"),
                ],
                default="not-specified",
                max_length=20,
            ),
        ),
    ]
