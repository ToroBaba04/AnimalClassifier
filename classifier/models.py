from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets


class UserProfile(models.Model):
    """Extended user profile with 2FA settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    two_fa_enabled = models.BooleanField(default=True)
    two_fa_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - 2FA: {'✓' if self.two_fa_enabled else '✗'}"


class TwoFactorToken(models.Model):
    """Temporary 2FA tokens for email verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='two_fa_tokens')
    token = models.CharField(max_length=6, unique=True)  # 6-digit code
    purpose = models.CharField(
        max_length=20,
        choices=[
            ('signup', 'Account Creation'),
            ('login', 'Login Verification'),
            ('update_email', 'Email Update')
        ],
        default='login'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        """Check if token is still valid"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"{self.user.username} - {self.purpose}"


class Classification(models.Model):
    """Image classification result with user ownership"""
    ANIMAL_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classifications', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    prediction = models.CharField(max_length=10, choices=ANIMAL_CHOICES, default='dog')
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Classifications'
    
    def __str__(self):
        return f"{self.user.username}: {self.prediction} ({self.confidence:.2%})"
