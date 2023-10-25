from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class User(AbstractUser):
    role_choices = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('not-specified', 'Not Specified'),
    )
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('not-specified', 'Not Specified')
    )
    role = models.CharField(max_length=20, choices=role_choices, default='not-specified')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(max_length=20, choices=gender_choices, blank=True, default='not-specified')
    joining_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('-joining_date',)
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
