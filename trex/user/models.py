from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    role = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    joining_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('-joining_date',)
        verbose_name_plural = 'Users'
        verbose_name = 'User'
