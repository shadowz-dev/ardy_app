# chat/models.py
from django.db import models
from django.conf import settings
# Create your models here.

class ChatRoom(models.Model):
    project = models.ForeignKey('core.projects',on_delete=models.CASCADE, related_name='chat_rooms')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_chats')
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider_chats')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)