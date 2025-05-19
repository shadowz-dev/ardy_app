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
            return self.subscription_history.get(is_active=True)
        except UserSubscription.DoesNotExist:
            return None
        except UserSubscription.MultipleObjectsReturned as e:
            print(e)
    

def company_profile_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/company_profiles/<company_name>/<year>/<month>/<day>/<filename>
    company_name = slugify(instance.company_name)
    return os.path.join('company_profiles', company_name, datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'), filename)

def customer_attachement_upload_path(instance, filename):
    # instance is a CustomerProfile instance
    user_name = slugify(instance.user.username)
    return os.path.join('customers', user_name, 'attachments', filename)

class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    introduction = models.TextField(blank=True)
    projects_completed = models.IntegerField(blank=True, null=True)
    company_profile = models.FileField(upload_to=company_profile_upload_path, blank=True)
    
    class Meta:
        abstract = True


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.IntegerField(blank=True)
    property_status = models.CharField(max_length=100, blank=True)
    project_details = models.TextField(blank=True)
    attachments = models.FileField(upload_to=customer_attachement_upload_path,blank=True)

    def __str__(self):
        return f"{self.user.username} - Customer Profile"

class ConsultantProfile(BaseProfile):
    def __str__(self):
        return f"{self.user.username} - Consultant Profile"

class InteriorProfile(BaseProfile):
    def __str__(self):
        return f"{self.user.username} - Interior Profile"

class ConstructionProfile(BaseProfile):
    def __str__(self):
        return f"{self.user.username} - Construction Profile"

class MaintainanceProfile(BaseProfile):
    def __str__(self):
        return f"{self.user.username} - Maintainance Profile"

class SmartHomeProfile(BaseProfile):
    def __str__(self):
        return f"{self.user.username} - SmartHome Profile"

#----------------------------------------------------------------Subscriptions-----------------------------------------------------

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50, choices=[('1', 'Customer'), ('2', 'Service Provider')])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(default=dict, help_text="JSON structure for features")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"
    
class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription_history')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, null=False,blank=False,default=1)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status_reason = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'} ({status})"
    
    def save(self, *args, **kwargs):
        if self.is_active and not self.pk: # Also set start_date if new and active
            self.start_date = timezone.now()

        if self.is_active:
            # Deactivate other active subscriptions for this user
            qs = UserSubscription.objects.filter(user=self.user, is_active=True)
            if self.pk: # If instance already exists, exclude it from the update
                qs = qs.exclude(pk=self.pk)
            qs.update(is_active=False, end_date=timezone.now())

        # If this subscription is being deactivated, ensure end_date is set
        if not self.is_active and self.pk: # Check original state if possible or just ensure end_date if not active
            original_instance = UserSubscription.objects.get(pk=self.pk)
            if original_instance.is_active: # If it was active and now is not
                self.end_date = timezone.now()

        super().save(*args, **kwargs)
    
    