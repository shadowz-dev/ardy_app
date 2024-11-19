from rest_framework import generics
from .models import User, CustomerProfile, ConsultantProfile, InteriorProfile, ConstructionProfile, MaintainanceProfile, SmartHomeProfile
from .serializers import UserSerializer, CustomerProfileSerializer, ConsultantProfileSerializer, InteriorProfileSerializer, ConstructionProfileSerializer, MaintainanceProfileSerializer, SmartHomeProfileSerializer
from rest_framework.response import Response
from .permission import IsCustomer, IsConsultant, IsConstruction, IsInterior, IsSmartHome, IsMaintainance
from knox.models import AuthToken
from knox.views import LoginView as knoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

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