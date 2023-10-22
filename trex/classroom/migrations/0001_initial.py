# Generated by Django 4.2.6 on 2023-10-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Classroom",
            fields=[
                ("classroom_id", models.AutoField(primary_key=True, serialize=False)),
                ("classroom_name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("classroom_code", models.CharField(max_length=20)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Classroom",
                "verbose_name_plural": "Classrooms",
                "ordering": ("classroom_id",),
            },
        ),
    ]
