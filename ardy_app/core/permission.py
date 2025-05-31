from rest_framework.permissions import BasePermission
from .constants import *

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "Customer"
    
class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and
                request.user.user_type == "Consultant" and 
                request.user.is_approved_provider)
    
class IsInterior(BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and
                request.user.user_type == "Interior Design" and 
                request.user.is_approved_provider)
    
class IsConstruction(BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and
                request.user.user_type == "Construction" and 
                request.user.is_approved_provider)
    
class IsMaintenance(BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and
                request.user.user_type == "Maintenance" and 
                request.user.is_approved_provider)
    
class IsSmartHome(BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and
                request.user.user_type == "Smart_Home" and 
                request.user.is_approved_provider)
    
class IsServiceProvider(BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.user_type in SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL and
                request.user.is_approved_provider)
    

class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and hasattr(user, 'subscription') and user.subscription.plan.name in ['Premium', 'VIP']
    
class IsProjectOwner(BasePermission):
    message = "You are not the owner of this project."
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        #Try to access the project through common attributes name
        project_instance = None
        if hasattr(obj, 'project'): # For Phase, Quotation, Drawing, Document
            project_instance = obj.project
        elif obj.__class__.__name__ == 'Projects': # If the object itself is a Project
            project_instance = obj
            
        if project_instance and hasattr(project_instance, 'customer') and project_instance.customer:
            return project_instance.customer.user == request.user
        
        return False
    
class IsPhaseAssignedServiceProvider(BasePermission):
    message = "You are not the service provider assigned to this phase."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        phase_instance = None
        if hasattr(obj, 'phase') and obj.phase:
            phase_instance = obj.phase
        elif obj.__class__.__name__ == 'Phase':
            phase_instance = obj
            
        if phase_instance and hasattr(phase_instance, 'service_provider') and phase_instance.service_provider:
            return phase_instance.service_provider == request.user
        
        return False
    
class IsObjectUploader(BasePermission): # Example for Drawings/Documents
    """
    Allows access only to the user who uploaded the object (e.g., Drawing, Document).
    Assumes obj has an 'uploaded_by' attribute.
    """
    message = "You are not the uploader of this item."

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(obj, 'uploaded_by') and obj.uploaded_by == request.user