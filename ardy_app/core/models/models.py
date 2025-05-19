# core/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime
from django.conf import settings

#Users Imports
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .project import *
from ..constants import *
from .user import *

    

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company')
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='company_employees', blank=True, through='EmployeeRelationship')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.company_name
    
class EmployeeRelationship(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ('company', 'employee')
        
        
    def __str__(self):
        return f"{self.employee.username} at {self.company.company_name}"


#----------------------------------------------------Start General Documents Model-----------------------------------------------




#----------------------------------------------------Start PhoneOTP Model-----------------------------------------------
class UserOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps',null=True,blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed."
    )
    phone= models.CharField(validators=[phone_regex], max_length=14, blank=False, null=False)
    email= models.EmailField(blank=False, null=False)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count= models.IntegerField(default=0, help_text="Number of OTP sent")
    otp_type = models.CharField(max_length=20, choices=UserOTP, default='signup')
    social_login_token = models.CharField(max_length=1000, blank=True, null=True, default=None)
    
    class Meta:
        unique_together = ('phone', 'email',)
    

    def __str__(self):
        return f"OTP for {self.user.username} ({self.otp_type})"
#-----------------------------------------------------End PhoneOTP Model------------------------------------------------

#----------------------------------------------------Start Subscription Model-----------------------------------------------


    
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

#----------------------------------------------------Start PromoCode & Referral Model-----------------------------------------------

class SubPromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_uses = models.IntegerField(default=1)
    uses = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.uses < self.max_uses and timezone.now() < self.end_date
    
    def __str__(self):
        return self.code
    
class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrerals')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by', null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    reward = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f"Referral by {self.referrer.username}"