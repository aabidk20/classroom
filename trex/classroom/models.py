from django.db import models

# Create your models here.


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    classroom_code = models.CharField(max_length=20, null=False)
    teacher = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='classrooms')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.classroom_name

    class Meta:
        ordering = ('classroom_id',)
        verbose_name_plural = 'Classrooms'
        verbose_name = 'Classroom'
