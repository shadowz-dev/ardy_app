# chat/urls.py
from django.urls import path, include
from chat.views import *
from . import consumers

app_name = 'chat'

urlpatterns = [
    path('ws/chat/<int:room_id>', consumers.ChatConsumer.as_asgi()),
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/create/', ChatRoomCreateView.as_view(), name='chatroom-create'),
    path('chatrooms/<int:room_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('chatrooms/<int:room_id>/messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/unread/', UnreadMessagesView.as_view(), name='unread-messages'),
]
