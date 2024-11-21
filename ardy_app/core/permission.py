from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type == "Customer"
    
class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type == "Consultant"
    
class IsInterior(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type == "Interior Designer"
    
class IsConstruction(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type == "Construction"
    
class IsMaintainance(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type == "Maintainance"
    
class IsSmartHome(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type == "Smart Home"
    
class IsServiceProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.user_type in ['Consultant','Interior Designer', 'Construction','Maintainance','Smart Home']