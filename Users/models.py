from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

priviledges = (
    ('admin', 'ADMIN'),
    ('superuser', 'SUPERUSER'),
    ('user', 'USER'),
)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(
        max_length=20, default="", blank=True, null=True)
    email = models.CharField(max_length=255, default="", blank=True, null=True)
    company = models.CharField(
        max_length=255, default="", blank=True, null=True)
    priviledge = models.CharField(
        max_length=255, choices=priviledges, default='user')
    profile_pic = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return self.user.username


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
