from django.db import models
from django.conf import settings
from apps.boards.models import Board

class Pin(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pins/')
    link = models.URLField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pins')
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, related_name='pins', blank=True, null=True)
    is_uploaded = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Pin"
