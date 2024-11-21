from rest_framework import serializers, status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .models import User, CustomerProfile, ConsultantProfile, InteriorProfile, ConstructionProfile, MaintainanceProfile, SmartHomeProfile
from .models import Quotation, Projects

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type','phone','first_name', 'last_name','birthday','newsletter','offers_and_discounts','date_joined','signup_type','social_login_token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['user','land_details','property_type','budget','property_status','project_details','attachments']

class ConsultantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class InteriorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteriorProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class ConstructionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class MaintainanceProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MaintainanceProfile 
        fields = ['user','company_name','expertise','experience','portfolio','introduction','jobs_completed','company_profile']

class SmartHomeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartHomeProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']


#---------------------------------------------------Quotations Serializer --------------------------------

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id', 'project', 'service_provider', 'stage', 'stage', 'details', 'amount', 'status', 'created_at', 'updated_at']