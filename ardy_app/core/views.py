# core/views.py
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from .permission import *
from knox.models import AuthToken
from knox.views import LoginView as knoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from .utils import apply_sub_promo_code
from decimal import Decimal
from rest_framework.exceptions import ValidationError

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user.user_type == 'Customer':
            CustomerProfile.objects.create(user=user)
        elif user.user_type == 'Consultant':
            ConsultantProfile.objects.create(user=user)
        elif user.user_type == 'Interior Designer':
            InteriorProfile.objects.create(user=user)
        elif user.user_type == 'Construction':
            ConstructionProfile.objects.create(user=user)
        elif user.user_type == 'Maintainance':
            MaintainanceProfile.objects.create(user=user)
        elif user.user_type == 'Smart Home':
            SmartHomeProfile.objects.create(user=user)
        else:
            raise ValueError('Invalid user type')

class CustomerProfileView(generics.RetrieveAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsCustomer]

class ConsultantProfileView(generics.RetrieveAPIView):
    queryset = ConsultantProfile.objects.all()
    serializer_class = ConsultantProfileSerializer
    permission_classes = [IsConsultant]

class InteriorProfileView(generics.RetrieveAPIView):
    queryset = InteriorProfile.objects.all()
    serializer_class = InteriorProfileSerializer
    permission_classes = [IsInterior]

class ConstructionProfileView(generics.RetrieveAPIView):
    queryset = ConstructionProfile.objects.all()
    serializer_class = ConstructionProfileSerializer
    permission_classes = [IsConstruction]

class MaintainanceProfileView(generics.RetrieveAPIView):
    queryset = MaintainanceProfile.objects.all()
    serializer_class = MaintainanceProfileSerializer
    permission_classes = [IsMaintainance]

class SmartHomeProfileView(generics.RetrieveAPIView):
    queryset = SmartHomeProfile.objects.all()
    serializer_class = SmartHomeProfileSerializer
    permission_classes = [IsSmartHome]


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serialzer = self.get_serializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        user = serialzer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
    
class LoginAPI(knoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    
#----------------------------------------------------------------Quotations Views----------------------------------------------------

class QuotationCreateView(generics.CreateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]

class QuotationListView(generics.ListAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuotationUpdateView(generics.UpdateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]

class QuotationApprovalView(generics.UpdateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def perform_update(self, serializer):
        serializer.save(status=self.request.data.get('status'))

class DrawingListView(generics.ListAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]

class DrawingUploadView(generics.CreateAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]

class RevisionRequestView(generics.CreateAPIView):
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

class DocumentListView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]


#----------------------------------------------------------------Subscription Views----------------------------------------------------
class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer

class SubscribeToPlanView(generics.CreateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        plan = serializer.validated_data('plan')
        promo_code = self.request.data.get('promo_code', None)

        discount_percent = 0
        if promo_code:
            discount_percent = apply_sub_promo_code(user, promo_code)

        discounted_price = Decimal(plan.price) * (1 - (discount_percent / 100))


        if plan.user_type == 'Customer' and user.user_type != 'Customer':
            raise serializers.ValidationError("This plan is for customers only.")
        if plan.user_type == 'Service Provider' and user.user_type == 'Customer':
            raise serializers.ValidationError("This plan is for service providers only.")
        
        if hasattr(user, 'subscription') and user.subscription.is_active:
            user.subscription.is_active = False
            user.subscription.save()

        serializer.save(user=user, is_active=True)

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class SubscriptionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'subscription') and not user.subscription.is_active:
            return JsonResponse({"error": "Your subscription has expired. Please renew your subscription."}, status=403)
        

class ApplySubPromoCodeView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        promo_code = request.data.get('promo_code')
        try:
            discount_percent = apply_sub_promo_code(request.user, promo_code)
            return Response({'success': True, 'discount_percent': discount_percent})
        except ValueError as e:
            raise ValidationError({'error': str(e)})
        
class ReferralListView(generics.ListAPIView):
    serializer_class = ReferralSerializer

    def get_queryset(self):
        return Referral.objects.filter(referrer = self.request.user)