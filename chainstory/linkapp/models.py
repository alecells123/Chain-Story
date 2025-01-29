from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#000000")  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class ChatMessage(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default="#000000")  # Store color at time of message
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content}"