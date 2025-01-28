from django.db import models

# Create your models here.

class ChatMessage(models.Model):
    content = models.TextField()
    username = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.content}"