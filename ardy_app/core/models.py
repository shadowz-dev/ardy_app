# core/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime

#Users Imports
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from .models.user import *
from .models.project import *
from .constants import *


    
#----------------------------------------------------Start Permission Groups Model-----------------------------------------------
class Command(BaseCommand):
    help = 'Create default user groups and permissions'

    def handle(self, *args, **kwargs):
        groups = {
            'Customers': [],
            'Consultants': ['can_submit_quotation', 'can_upload_drawings'],
            'Construction': ['can_submit_quotation','can_update_project_phases'],
            'InteriorDesigners': ['can_submit_quotation','can_upload_designes'],
            'Admins': ['can_approve_users', 'can_manage_projects'],
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in permissions:
                permission, _ = Permission.objects.get_or_create(
                    name=f"Can {perm_codename.replace('-', ' ')}",
                    content_type=ContentType.objects.get_for_model(User),
                )
                group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' updated"))
        self.stdout.write(self.style.SUCCESS("Groups and permissions set up"))



class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    employees = models.ManyToManyField(User, related_name='company_employees', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


#----------------------------------------------------Start General Documents Model-----------------------------------------------




#----------------------------------------------------Start PhoneOTP Model-----------------------------------------------
class PhoneOTP(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=14, blank=False, null=False, unique=True)
    password = models.CharField(default=0, blank=False, null=False, max_length=50)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if validate otp forgot get successful')
    referral_code = models.CharField(max_length=200, blank=True, null=True, unique=False)
    signup_type = models.CharField(default="Manual", max_length=6, choices=SIGNUP_TYPE, help_text='Type of Signup.')
    social_login_token = models.CharField(max_length=1000, blank=True, null=True, default=None)
    notification_token = models.CharField(default=None, blank=True, null=True, max_length=300, unique=True, help_text='We will send the notification via this token.')

    def __str__(self):
        return str(self.email) + ' is sent ' + str(self.otp)
#-----------------------------------------------------End PhoneOTP Model------------------------------------------------

#----------------------------------------------------Start Subscription Model-----------------------------------------------

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100, default='Free', choices=[('Free', 'Free'), ('Premium', 'Premium')])
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} Plan"
    
#----------------------------------------------------End Subscription Model-----------------------------------------------


class Lead(models.Model):
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False) # If the lead is got using paid methods

    def __str__(self):
        return f"Lead for {self.project.title} - {self.service_provider.username}"
    

class Milestone(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Milestone for {self.title}: {self.title}"
    
class Review(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.service_provider.username} by {self.customer.user.username}"
    

class FeaturedListing(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Featured Listing - {self.profile.username}"
    
class EngagementLog(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50) # view , click , reveiew 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - on {self.profile.username} at {self.timestamp}"
    



    

#----------------------------------------------------Start Transactions Model-----------------------------------------------

class Transaction(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_maker')
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_receiver')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    phase = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)

#----------------------------------------------------End Transactions Model-----------------------------------------------

#----------------------------------------------------Start Notifications Model-----------------------------------------------
