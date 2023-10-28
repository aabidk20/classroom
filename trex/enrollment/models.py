from django.db import models

# Create your models here.


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='enrollments')

    def __str__(self):
        return f"{self.student} - {self.classroom}"

    class Meta:
        ordering = ('enrollment_id',)
        verbose_name_plural = 'Enrollments'
        verbose_name = 'Enrollment'
        unique_together = ('classroom', 'student')

