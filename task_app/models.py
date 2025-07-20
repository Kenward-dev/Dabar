"""This module contains models for the Taskly application, including a custom user model and a task model."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser to include additional fields if needed.
    """
    email = models.EmailField(unique=True, verbose_name=_("email address"))
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Task(models.Model):
    """Model representing a task in the task management application."""
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks', verbose_name=_("owner"))
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title