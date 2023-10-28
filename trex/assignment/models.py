from django.db import models

# Create your models here.


class Assignment(models.Model):
    status_choices = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=status_choices, default='draft')
    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.CASCADE, related_name='assignments')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ('created_on', 'assignment_id')
        verbose_name_plural = 'Assignments'
        verbose_name = 'Assignment'
