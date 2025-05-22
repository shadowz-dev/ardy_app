from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from .constants import *

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer # Used by Knox LoginView

from .models.user import (
    User, CustomerProfile, ConsultantProfile, InteriorProfile, ConstructionProfile,
    MaintenanceProfile, SmartHomeProfile, SubscriptionPlan, UserSubscription
)
from .models import Referral
from .models.project import (
    Projects, Phase, Quotation, Drawing, Revision, Document
)
from .serializers import (
    UserSerializer, CustomerProfileSerializer, ConsultantProfileSerializer, InteriorProfileSerializer,
    ConstructionProfileSerializer, MaintenanceProfileSerializer, SmartHomeProfileSerializer,
    SubscriptionPlanSerializer, UserSubscriptionSerializer, ReferralSerializer,
    ProjectsSerializer, PhaseSerializer, QuotationSerializer, DrawingSerializer,
    RevisionSerializer, DocumentSerializer, SubPromoCodeSerializer
)
from .permission import ( # Assuming these are defined
    IsCustomer, IsConsultant, IsInterior, IsConstruction,
    IsMaintenance, IsSmartHome, IsServiceProvider
)
from .utils import apply_sub_promo_code # Assuming this utility exists


# --- User Authentication & Registration ---



class RegisterAPIView(generics.CreateAPIView): # Renamed from RegisterAPI
    """
    Handles new user registration.
    Profile creation is handled by signals.
    Returns user data and auth token.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Profile creation should be handled by a post_save signal on User model
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1] # AuthToken.objects.create returns a tuple (instance, token)
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(KnoxLoginView):
    """
    Handles user login using Knox for token authentication.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        
        serializer = AuthTokenSerializer(data=request.data) # Standard DRF AuthTokenSerializer for credentials
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user) # Standard Django login
        return super().post(request, format=None) # KnoxLoginView handles token generation


# --- Profile Views ---
# Using RetrieveUpdateAPIView for users to view and update their own profiles.

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Users can only retrieve/update their own profile.
        # self.queryset should be set by the subclass (e.g., CustomerProfile.objects.all())
        profile_model = self.queryset.model # Gets the model class (e.g., CustomerProfile)
        try:
            return profile_model.objects.get(user=self.request.user)
        except profile_model.DoesNotExist:
            # Or raise Http404 if profile must exist
            raise PermissionDenied("Profile not found or you do not have permission to access it.")

    def perform_update(self, serializer):
        serializer.save(user=self.request.user) # Ensure user is not changed on update

class CustomerProfileDetailView(UserProfileView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer] # Ensure only customers can access

class ConsultantProfileDetailView(UserProfileView): 
    queryset = ConsultantProfile.objects.all()
    serializer_class = ConsultantProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultant]

class InteriorProfileDetailView(UserProfileView):
    queryset = InteriorProfile.objects.all()
    serializer_class = InteriorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsInterior]

class ConstructionProfileDetailView(UserProfileView):
    queryset = ConstructionProfile.objects.all()
    serializer_class = ConstructionProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsConstruction]

class MaintenanceProfileDetailView(UserProfileView):
    queryset = MaintenanceProfile.objects.all()
    serializer_class = MaintenanceProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsMaintenance]

class SmartHomeProfileDetailView(UserProfileView):
    queryset = SmartHomeProfile.objects.all()
    serializer_class = SmartHomeProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsSmartHome]


# --- Project & Phase Management (ModelViewSet is good for RESTful CRUD) ---

class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    permission_classes = [permissions.IsAuthenticated] # Add more specific permissions

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Customer':
            return Projects.objects.filter(customer__user=user)
        elif user.user_type in ['Consultant', 'Construction', 'Interior Designer', 'Maintenance', 'Smart Home']:
            # Service providers see projects they are primary on or assigned to a phase in
            return Projects.objects.filter(
                Q(primary_service_provider=user) | Q(phases__service_provider=user)
            ).distinct()
        elif user.is_staff or user.user_type == 'Admin': # Admin/staff can see all
            return Projects.objects.all()
        return Projects.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type != 'Customer':
            raise PermissionDenied("Only customers can create projects.")
        try:
            customer_profile = CustomerProfile.objects.get(user=self.request.user)
            serializer.save(customer=customer_profile)
        except CustomerProfile.DoesNotExist:
            raise ValidationError("Customer profile not found for the current user.")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCustomer]) # Or admin
    def start(self, request, pk=None):
        project = self.get_object()
        initial_phase_id = request.data.get('initial_phase_id')
        initial_phase = None
        if initial_phase_id:
            try:
                initial_phase = project.phases.get(id=initial_phase_id)
            except Phase.DoesNotExist:
                return Response({"error": "Initial phase not found for this project."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            project.start_project(initial_phase=initial_phase)
            return Response(ProjectsSerializer(project, context={'request': request}).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCustomer]) # Or admin
    def advance_phase(self, request, pk=None):
        project = self.get_object()
        target_phase_id = request.data.get('target_phase_id')
        new_sp_id = request.data.get('service_provider_id') 

        if not target_phase_id:
            return Response({"error": "target_phase_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target_phase = project.phases.get(id=target_phase_id)
            service_provider = None
            if new_sp_id:
                service_provider = User.objects.get(id=new_sp_id)
                if service_provider.user_type == 'Customer':
                    raise ValueError("Cannot assign a Customer as a service provider for a phase.")
            project.advance_to_phase(target_phase, new_service_provider_for_target_phase=service_provider)
            return Response(ProjectsSerializer(project, context={'request': request}).data, status=status.HTTP_200_OK)
        except (Phase.DoesNotExist, User.DoesNotExist) as e:
            return Response({"error": "Target phase or service provider not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCustomer]) # Or admin
    def complete(self, request, pk=None):
        project = self.get_object()
        force_complete = request.data.get('force_complete', False)
        try:
            project.complete_project(force_complete=force_complete)
            return Response(ProjectsSerializer(project, context={'request': request}).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCustomer]) # Or admin
    def cancel(self, request, pk=None):
        project = self.get_object()
        reason = request.data.get('reason', "")
        try:
            project.cancel_project(reason=reason)
            return Response(ProjectsSerializer(project, context={'request': request}).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PhaseViewSet(viewsets.ModelViewSet):
    serializer_class = PhaseSerializer
    permission_classes = [permissions.IsAuthenticated] # Add more specific permissions

    def get_queryset(self):
        user = self.request.user
        project_id = self.request.query_params.get('project_id') or self.kwargs.get('project_pk')
        
        queryset = Phase.objects.all()
        if project_id:
            queryset = queryset.filter(project_id=project_id)
            try:
                project = Projects.objects.get(id=project_id)
                if not (project.customer.user == user or
                        (project.primary_service_provider == user) or
                        project.phases.filter(service_provider=user).exists() or
                        user.is_staff):
                    return Phase.objects.none() # Not related to this project
            except Projects.DoesNotExist:
                return Phase.objects.none()
        else: # If not filtering by project, apply general user-based filtering
            if user.user_type == 'Customer':
                queryset = queryset.filter(project__customer__user=user)
            elif user.user_type in ['Consultant', 'Construction', 'Interior Designer', 'Maintenance', 'Smart Home']:
                queryset = queryset.filter(service_provider=user)
            elif not user.is_staff: # Non-admin, non-customer, non-SP shouldn't see any by default
                return Phase.objects.none()
        return queryset

    def perform_create(self, serializer):
        project_id = serializer.validated_data.get('project').id # Assuming project is passed as ID
        try:
            project = Projects.objects.get(id=project_id)
            # Check if request.user is customer of this project or admin
            if not (project.customer.user == self.request.user or self.request.user.is_staff):
                raise PermissionDenied("You cannot add phases to this project.")
            serializer.save() # Project is already in validated_data
        except Projects.DoesNotExist:
            raise ValidationError("Project not found.")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated]) # Perms: SP of phase or Customer of project
    def complete_phase_action(self, request, pk=None): # Renamed to avoid clash
        phase = self.get_object()
        if not (phase.service_provider == request.user or phase.project.customer.user == request.user or request.user.is_staff):
            raise PermissionDenied("You are not authorized to complete this phase.")
        try:
            project = phase.project # Get the project instance from the phase
            project.complete_phase(phase_to_complete=phase) # Call the method on project instance
            return Response(PhaseSerializer(phase, context={'request': request}).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- Quotation Views ---

class QuotationViewSet(viewsets.ModelViewSet):
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Customer':
            return Quotation.objects.filter(project__customer__user=user)
        elif user.user_type in ['Consultant', 'Construction', 'Interior Designer', 'Maintenance', 'Smart Home']:
            return Quotation.objects.filter(service_provider=user)
        elif user.is_staff:
            return Quotation.objects.all()
        return Quotation.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type == 'Customer':
            raise PermissionDenied("Customers cannot create quotations.")
        serializer.save(service_provider=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCustomer])
    def approve(self, request, pk=None):
        quotation = self.get_object()
        try:
            # Ensure the user approving is the customer of the project linked to the quotation
            if quotation.project.customer.user != request.user:
                raise PermissionDenied("You are not authorized to approve this quotation.")
            quotation.approve(approving_user=request.user)
            return Response(QuotationSerializer(quotation, context={'request': request}).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCustomer])
    def reject(self, request, pk=None):
        quotation = self.get_object()
        reason = request.data.get("reason", "")
        try:
            if quotation.project.customer.user != request.user:
                raise PermissionDenied("You are not authorized to reject this quotation.")
            quotation.reject(rejecting_user=request.user, reason=reason)
            return Response(QuotationSerializer(quotation, context={'request': request}).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- Drawing, Revision, Document Views ---

class DrawingViewSet(viewsets.ModelViewSet):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter based on user's projects or if they are the uploader
        user = self.request.user
        if user.user_type == 'Customer':
            return Drawing.objects.filter(project__customer__user=user)
        # Add logic for service providers to see drawings they uploaded or for projects they are on
        return Drawing.objects.filter(Q(project__customer__user=user) | Q(uploaded_by=user) | Q(project__phases__service_provider=user)).distinct()


    def perform_create(self, serializer):
        if self.request.user.user_type == 'Customer':
            raise PermissionDenied("Customers cannot directly upload drawings.")
        # Add logic to link project and phase correctly from request.data if not directly in serializer
        serializer.save(uploaded_by=self.request.user)


class RevisionViewSet(viewsets.ModelViewSet):
    serializer_class = RevisionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Customers see revisions they requested. Service providers see revisions for their drawings.
        user = self.request.user
        if user.user_type == 'Customer':
            return Revision.objects.filter(customer__user=user)
        return Revision.objects.filter(drawing__uploaded_by=user) # Or drawing__phase__service_provider

    def perform_create(self, serializer):
        if self.request.user.user_type != 'Customer':
            raise PermissionDenied("Only customers can request revisions.")
        try:
            customer_profile = CustomerProfile.objects.get(user=self.request.user)
            # Ensure drawing being revised belongs to a project of this customer
            drawing_id = serializer.validated_data.get('drawing').id
            drawing = Drawing.objects.get(id=drawing_id)
            if drawing.project.customer != customer_profile:
                raise PermissionDenied("You can only request revisions for drawings on your projects.")
            serializer.save(customer=customer_profile)
        except CustomerProfile.DoesNotExist:
            raise ValidationError("Customer profile not found.")
        except Drawing.DoesNotExist:
            raise ValidationError("Drawing not found.")


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        project_id_param = self.request.query_params.get('project_id')

        if user.is_staff or user.user_type == 'Admin':
            if project_id_param:
                return Document.objects.filter(project_id=project_id_param)
            return Document.objects.all()

        if user.user_type == 'Customer':
            # Customers see all documents for projects they own
            queryset = Document.objects.filter(project__customer__user=user)
            if project_id_param: # If they specify a project_id, filter further
                return queryset.filter(project_id=project_id_param)
            return queryset # Otherwise, show docs from all their projects

        elif user.user_type in SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL: # Use your constant
            # SPs see documents they uploaded, or for projects they are primary on,
            # or for phases they are assigned to.
            q_filters = Q(uploaded_by=user) | \
                        Q(project__primary_service_provider=user) | \
                        Q(phase__service_provider=user)
            
            queryset = Document.objects.filter(q_filters).distinct()
            if project_id_param:
                return queryset.filter(project_id=project_id_param)
            return queryset
        
        return Document.objects.none() # Default for other unhandled roles

    def perform_create(self, serializer):
        user = self.request.user
        # Allow customers to upload general project documents (no specific phase or their own phase)
        # Allow service providers to upload documents to their assigned phases or projects
        
        # Example: Basic check - refined logic needed based on your rules
        # For now, let's assume customers CAN upload documents.
        # The more specific permission about *what kind* of document or *where*
        # might be handled by serializer validation or more complex permission classes.

        # If you want to restrict based on phase:
        phase_instance = serializer.validated_data.get('phase')
        if phase_instance and user.user_type == 'Customer':
            raise PermissionDenied("Customers can only upload general project documents, not for specific phases managed by SPs.")
        elif phase_instance and user != phase_instance.service_provider and not user.is_staff:
            raise PermissionDenied("You can only upload documents to phases you are assigned to.")

        serializer.save(uploaded_by=user) # General allowance for now


# --- Subscription Views ---

class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny] # Usually public to see plans

class SubscribeToPlanView(generics.CreateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        plan = serializer.validated_data.get('plan')
        # promo_code = self.request.data.get('promo_code', None) # Promo code logic might be separate

        # Validate plan choice against user type
        # Example: '1' for Customer, '2' for Service Provider in SubscriptionPlan.user_type
        if plan.user_type == '1' and user.user_type != 'Customer':
            raise ValidationError("This plan is for customers only.")
        if plan.user_type == '2' and user.user_type == 'Customer': # Assuming '2' maps to SP
            raise ValidationError("This plan is for service providers only.")
        
        # Deactivate existing active subscription (if UserSubscription.save() doesn't handle it)
        # UserSubscription.objects.filter(user=user, is_active=True).update(is_active=False, end_date=timezone.now())
        
        serializer.save(user=user, is_active=True, start_date=timezone.now()) # Explicitly set start_date

# (SubscriptionMiddleware and ApplySubPromoCodeView can remain similar, ensure apply_sub_promo_code is robust)
# (ReferralListView can remain similar)

class ApplySubPromoCodeView(generics.GenericAPIView): # Changed from CreateAPIView if only post is needed
    # serializer_class = SubPromoCodeSerializer # Optional if not directly using it for input validation here
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        promo_code_value = request.data.get('promo_code') # Changed from 'promo_code' to avoid clash if serializer used this
        if not promo_code_value:
            return Response({'error': 'Promo code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Assuming apply_sub_promo_code takes the user and the code string
            discount_percent = apply_sub_promo_code(request.user, promo_code_value)
            return Response({'success': True, 'discount_percent': discount_percent}, status=status.HTTP_200_OK)
        except ValueError as e: # Catch specific errors from your utility
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: # General catch
            return Response({'error': 'An unexpected error occurred processing the promo code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReferralListView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own referrals (referrals they made)
        return Referral.objects.filter(referrer=self.request.user)