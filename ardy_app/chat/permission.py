from rest_framework.permissions import BasePermission
from chat.models import ChatRoom, Message

class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        room = ChatRoom.objects.get(id=view.kwargs['room_id'])
        return request.user == room.customer or request.user == room.service_provider
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'Customer'