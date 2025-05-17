# core/models/user.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from ..constants import *
import os


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
    date_joined = models.DateTimeField(verbose_name=("date joined"), default=timezone.now)
    

    def __str__(self):
        return f"{self.username} - ({self.user_type})"
    

def company_profile_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/company_profiles/<company_name>/<year>/<month>/<day>/<filename>
    company_name = instance.company_name
    return os.path.join('company_profiles', company_name, datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'), filename)

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
    attachments = models.FileField(upload_to='customers/attachments',blank=True)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, null=False,blank=False,default=1)
    start_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'plan'], name='unique_user_subscription')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"
    
    