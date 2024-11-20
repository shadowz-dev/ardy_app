# chat/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/project/<int:project_id>/', consumers.ChatConsumer.as_asgi()), # Dynamic Room name
]