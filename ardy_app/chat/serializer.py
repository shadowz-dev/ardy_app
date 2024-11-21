from rest_framework import serializers
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'customer', 'service_provider', 'customer_name', 'service_provider_name', 'created_at']
        read_only_fields = ['id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'receiver', 'sender_name', 'receiver_name', 'content', 'timestamp', 'read']
        read_only_fields = ['id', 'timestamp', 'read']

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']

    def create(self, validated_data):
        request = self.context['request']
        room = self.context['room']
        sender = request.user
        receiver = room.service_provider if sender == room.customer else room.customer

        return Message.objects.create(
            room=room,
            sender=sender,
            receiver=receiver,
            content=validated_data['content']
        )