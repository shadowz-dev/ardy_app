from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import *

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type','phone','first_name', 'last_name','birthday','news_letter','offers_and_discounts','date_joined']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class LandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandDetail
        fields = '__all__'
    
class CustomerProfileSerializer(serializers.ModelSerializer):
    land_details = LandDetailSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = CustomerProfile
        fields = ['user','budget','property_status','project_details','attachments','land_details']

class ConsultantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ConsultantProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class InteriorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = InteriorProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class ConstructionProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ConstructionProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class MaintenanceProfileSerializer(serializers.ModelSerializer):  
    user = UserSerializer(read_only=True)
    class Meta:
        model = MaintenanceProfile 
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

class SmartHomeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = SmartHomeProfile
        fields = ['user','company_name','expertise','experience','portfolio','introduction','projects_completed','company_profile']

#---------------------------------------------------Subscription Serializer --------------------------------
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'user_type', 'price', 'features', 'is_active']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan_details = SubscriptionPlanSerializer(source="plan", read_only=True)
    
    class Meta:
        model = UserSubscription
        fields = ['id', 'user', 'plan', 'plan_details', 'start_date', 'end_date','is_active']



#---------------------------------------------------Quotations Serializer --------------------------------
class PhaseSerializer(serializers.ModelSerializer):
    service_provider_username = serializers.CharField(source='service_provider.username', read_only=True)
    class Meta:
        model = Phase
        fields = ['id', 'project', 'service_provider','service_provider_username' , 'title', 'order', 'status', 'start_date', 'expected_end_date', 'actual_end_date']
        read_only_fields = ['project']
        
        
class QuotationSerializer(serializers.ModelSerializer):
    phase_id = serializers.PrimaryKeyRelatedField(queryset=Phase.objects.all(), source='phase', write_only=True)
    phase_details = PhaseSerializer(source='phase', read_only=True)
    service_provider = UserSerializer(read_only=True)
    class Meta:
        model = Quotation
        fields = ['id', 'project', 'phase_id','phase_details', 'service_provider', 'type', 'details', 'amount', 'status', 'submitted_at', 'updated_at', 'approved_at']
        read_only_fields = ['submitted_at', 'updated_at', 'phase_details']

class ProjectsSerializer(serializers.ModelSerializer):
    phases = PhaseSerializer(many=True, read_only=True)
    active_phase_details = PhaseSerializer(source='active_phase', read_only=True)
    customer = CustomerProfileSerializer(read_only=True)
    customer_username = serializers.CharField(source='customer.user.username', read_only=True)
    land_detail_info = LandDetailSerializer(source='land_detail', read_only=True)
    entry_point_service_name = serializers.CharField(write_only=True, required=False, allow_blank=True, help_text="Name of the ServiceType where the project should effectively start.")
    
    class Meta:
        model = Projects
        fields = [
            'id', 'customer', 'primary_service_provider', 
            'land_detail', 'land_detail_info', 'title', 'description',
            'status','active_phase', 'active_phase_details' , 
            'start_date', 'expected_end_date', 'actual_end_date',
            'phases', 'customer_username', 'entry_point_service_name'
        ]
        read_only_fields = ('status','active_phase_details' , 'start_date', 'actual_end_date')
        
class LandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandDetail
        fields = '__all__'

#---------------------------------------------------Drawing Serializer --------------------------------

class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', 'project', 'phase', 'uploaded_by', 'title', 'version', 'file', 'created_at', 'notes']
        read_only_fields = ['created_at']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'drawing', 'customer', 'comment', 'requested_at', 'resolved','resolved_at']
        read_only_fields = ['customer', 'requested_at', 'resolvet_at', 'resolved']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'project', 'phase', 'uploaded_by', 'title', 'file', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class SubPromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPromoCode
        fields = ['id', 'code', 'discount_percentage', 'max_uses', 'uses', 'start_date', 'end_date', 'is_active']

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred_user', 'code', 'reward', 'is_redeemed']


