# core/models/user.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from ..constants import *
import os
from django.conf import settings
from django.utils.text import slugify


class User(AbstractUser):
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format : '+99999999999'. Up to 14 digits allowed.",)
    phone = models.CharField(validators=[phone_regex], max_length=14, blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_approved_provider = models.BooleanField(default=False, help_text="True if this service provider application has been reviewed by ardy admin.")

    # Default users fields.
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    news_letter = models.BooleanField(default=False)
    offers_and_discounts = models.BooleanField(default=False)
    #date_joined = models.DateTimeField(verbose_name=("date joined"), default=timezone.now)
    

    def __str__(self):
        return f"{self.username} - ({self.get_user_type_display()})"
    
    @property
    def active_subscription(self):
        try:
            from .models import UserSubscription as UserSubscriptionModel
            return self.subscription_history.get(is_active=True)
        except UserSubscriptionModel.DoesNotExist:
            return None
        except UserSubscriptionModel.MultipleObjectsReturned as e:
            print(f"Error: Multiple active Subscriptions found for user {self.username}: {e}")
            return self.subscription_history.filter(is_active=True).first()


class ServiceType(models.Model):
        name = models.CharField(max_length=100, unique=True)
        description = models.TextField(blank=True)
        category = models.CharField(max_length=50, choices=USER_TYPES)
        
        # New fields for dynamic phase setup:
        default_order = models.PositiveIntegerField(
            default=1000, # Default to a high number if not part of standard flow
            help_text="Default order in a standard project lifecycle (lower numbers first). Use unique numbers for standard flow."
        )
        is_standard_phase_service = models.BooleanField(
            default=False,
            help_text="Include this service type when setting up standard project phases?"
        )
        default_phase_title_template = models.CharField(
            max_length=150,
            blank=True, null=True,
            help_text="Template for the phase title, e.g., 'Initial {} Design'. '{}' will be project title."
        )
        default_phase_description_template = models.TextField(
            blank=True, null=True,
            help_text="Template for the phase description. '{}' will be project title."
        )
        
        class Meta:
            ordering = ['default_order', 'name']
        
        def __str__(self):
            return self.name

def company_profile_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/company_profiles/<company_name>/<year>/<month>/<day>/<filename>
    company_name = slugify(instance.company_name if instance.company_name else "unkown_company")
    owner_id_str = str(instance.owner_id) if instance.owner_id else "no_owner"
    date_path = timezone.now().strftime("%Y/%m/%d")
    return os.path.join('company_profiles', owner_id_str, company_name, date_path, filename)

def customer_attachement_upload_path(instance, filename):
    # instance is a CustomerProfile instance
    user_name = slugify(instance.user.username)
    date_path = timezone.now().strftime("%Y/%m/%d")
    return os.path.join('customers', user_name, 'attachments', date_path ,filename)

class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True, null=True, help_text="Years of experience")
    portfolio = models.URLField(blank=True, null=True)
    introduction = models.TextField(blank=True)
    projects_completed = models.IntegerField(blank=True, null=True)
    company_profile = models.FileField(upload_to=company_profile_upload_path, blank=True, null=True, verbose_name="Company Profile Document")
    
    services_offered = models.ManyToManyField(ServiceType, blank=True, related_name="%(class)s_providers", help_text="Select the services you offer.")
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"Profile for {self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    budget = models.IntegerField(blank=True, default=0)
    property_status = models.CharField(max_length=100, blank=True)
    project_details = models.TextField(blank=True)
    attachments = models.FileField(upload_to=customer_attachement_upload_path,blank=True)

    def __str__(self):
        return f"{self.user.username} - Customer Profile"

class ConsultantProfile(BaseProfile):
    pass
class InteriorProfile(BaseProfile):
    pass
class ConstructionProfile(BaseProfile):
    pass
class MaintenanceProfile(BaseProfile):
    pass
class SmartHomeProfile(BaseProfile):
    pass
#----------------------------------------------------------------Subscriptions-----------------------------------------------------

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50, choices=[('1', 'Customer'), ('2', 'Service Provider')])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(default=dict, help_text="JSON structure for features")
    display_priority = models.IntegerField(default=100, help_text="Lower numbers show higher in listings (ex: 10=VIP, 20=Premium, 100=Free)")
    is_active = models.BooleanField(default=True)
    is_default_free_plan = models.BooleanField(default=False, unique=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"
    
    def get_default_subscription_plan_pk():
        try:
            plan = SubscriptionPlan.objects.get(is_default_free_plan=True)
            return plan.pk
        except SubscriptionPlan.DoesNotExist:
            return None
        except SubscriptionPlan.MultipleObjectsReturned:
            # Log error, this shouldn't happen
            return SubscriptionPlan.objects.filter(is_default_free_plan=True).first().pk if SubscriptionPlan.objects.filter(is_default_free_plan=True).exists() else None
    
class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription_history')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status_reason = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'} ({status})"
    
    def save(self, *args, **kwargs):
        # If this is a new active subscription, ensure start_date is set
        if self.is_active and not self.pk: # If new instance being marked active
            if not self.start_date: # Or if start_date not already set
                self.start_date = timezone.now()
            # Deactivate others only if this one is explicitly being made active
            UserSubscription.objects.filter(user=self.user, is_active=True).exclude(pk=self.pk).update(is_active=False, end_date=timezone.now())

        # If this subscription is being explicitly deactivated (and it was active)
        if not self.is_active and self.pk:
            try:
                original_instance = UserSubscription.objects.get(pk=self.pk)
                if original_instance.is_active: # If it was active and now is not
                    if not self.end_date: # Set end_date if not already set
                        self.end_date = timezone.now()
            except UserSubscription.DoesNotExist:
                pass # Should not happen if self.pk exists

        super().save(*args, **kwargs)
    
    
