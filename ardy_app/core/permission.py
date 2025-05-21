from rest_framework.permissions import BasePermission
from .constants import *

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Customer"
    
class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Consultant"
    
class IsInterior(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Interior Designer"
    
class IsConstruction(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Construction"
    
class IsMaintenance(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Maintenance"
    
class IsSmartHome(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Smart Home"
    
class IsServiceProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL
    

class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and hasattr(user, 'subscription') and user.subscription.plan.name in ['Premium', 'VIP']