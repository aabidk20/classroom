import os

from django.db import models


# Create your models here.

def get_upload_path(instance, filename):
    classroom_name = instance.submission.assignment.classroom.classroom_name
    classroom_id = instance.submission.assignment.classroom.classroom_id
    student_username = instance.submission.student.username
    assignment_id = instance.submission.assignment.assignment_id

    path = os.path.join("submissions",
                        f"{classroom_name}_{classroom_id}",
                        student_username,
                        f"{assignment_id}_{filename}").replace(" ", "_")
    return path


class Submission(models.Model):
    status_choices = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
    ]

    submission_id = models.AutoField(primary_key=True)
    submission_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_choices, default="draft")

    assignment = models.ForeignKey("assignment.Assignment", on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="submissions")

    def __str__(self):
        return f"{self.student} - {self.assignment}"

    class Meta:
        ordering = ['submission_time']
        verbose_name_plural = 'Submissions'
        verbose_name = 'Submission'


class SubmissionFile(models.Model):
    submission_file_id = models.AutoField(primary_key=True)
    submission = models.ForeignKey("submission.Submission", on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_upload_path, max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.file.name}"

    class Meta:
        ordering = ['submission_file_id']
        verbose_name_plural = 'Submission Files'
        verbose_name = 'Submission File'
