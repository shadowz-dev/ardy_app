from rest_framework import generics, permissions
from .models import ChatRoom, Message
from chat.serializer import *
from .permission import IsParticipant, IsCustomer
from django.db.models import Q

class ChatRoomCreateView(generics.CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def perform_create(self, serializer):
        # Ensure the chat room is unique between customer and service provider
        customer = self.request.user
        service_provider = self.request.data.get('service_provider')

        if ChatRoom.objects.filter(customer=customer, service_provider_id=service_provider).exists():
            raise serializers.ValidationError("ChatRoom already exists between these users.")

        serializer.save(customer=customer)

class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return chat rooms where the user is either the customer or service provider
        return ChatRoom.objects.filter(Q(customer=user) | Q(service_provider=user))
    

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        # Ensure the user is a participant in the chat room
        room = ChatRoom.objects.get(id=room_id)
        user = self.request.user
        if room.customer != user and room.service_provider != user:
            raise permissions.PermissionDenied("You are not a participant in this chat room.")
        return Message.objects.filter(room=room)

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        room = ChatRoom.objects.get(id=room_id)
        sender = self.request.user

        # Ensure the user is a participant in the chat room
        if room.customer != sender and room.service_provider != sender:
            raise permissions.PermissionDenied("You are not allowed to send messages in this chat room.")

        receiver = room.service_provider if sender == room.customer else room.customer
        serializer.save(room=room, sender=sender, receiver=receiver)



class UnreadMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user, read=False)
