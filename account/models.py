from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class AppUser(AbstractUser):
  phone_no = models.CharField(max_length=15, blank=True, null=True)
  is_customer=models.BooleanField(default=False)


class PasswordResetToken(models.Model):
    """Model to store password reset tokens"""
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset token for {self.user.email}"
