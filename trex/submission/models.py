from django.db import models

# Create your models here.


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
