# models/pinned_resource.py
from django.db import models
from django.contrib.auth.models import User
from .profile import Profile  # Import Profile from your existing file

class PinnedResource(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='pinned_resources'
    )
    title = models.CharField(max_length=200)
    resource_id = models.CharField(max_length=100, default='')  # ✅ Add this for unpin
    url = models.URLField(max_length=500)           # Actual URL for Visit button
    description = models.TextField(blank=True)
    pinned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-pinned_at']
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.title}"