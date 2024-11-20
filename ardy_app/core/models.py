# core/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime

#Users Imports
from django.contrib.auth.models import AbstractUser

USER_TYPES = [('Customer', 'Customer'), ('Consultant', 'Consultant'),
            ('Interior Designer', 'Interior Designer'), ('Construction', 'Construction'),
            ('Maintainance', 'Maintainance'),('Smart_Home', 'Smart_Home')]

SIGNUP_TYPE = [
    ("Manual", "Manual"),
    ("Google", "Google"),
    ("Apple", "Apple"),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled')
]
class User(AbstractUser):
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format : '+99999999999'. Up to 14 digits allowed.",)
    phone = models.CharField(validators=[phone_regex], max_length=14, blank=False, null=False, unique=True)
    signup_type = models.CharField(default="Manual", max_length=6, choices=SIGNUP_TYPE, help_text='Type of Signup.')

    # Default users fields.
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    news_letter = models.BooleanField(default=False)
    offers_and_discounts = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name=("date joined"), default=timezone.now)
    

    def __str__(self):
        return f"{self.username} - ({self.user_type})"
    
    # Seperate profiles for each user type
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.IntegerField(blank=True)
    property_status = models.CharField(max_length=100, blank=True)
    project_details = models.TextField(blank=True)
    attachments = models.FileField(upload_to='customers/attachments',blank=True)

    def __str__(self):
        return f"{self.user.username} - Customer Profile"

class ConsultantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True)
    portfolio = models.URLField(blank=True)
    introduction = models.TextField(blank=True)
    projects_completed = models.IntegerField(blank=True)
    company_profile = models.FileField(upload_to='company_profiles/consultants/', blank=True)

class InteriorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True)
    portfolio = models.URLField(blank=True)
    introduction = models.TextField(blank=True)
    projects_completed = models.IntegerField(blank=True)
    company_profile = models.FileField(upload_to='company_profiles/interiors/', blank=True)

class ConstructionProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True)
    portfolio = models.URLField(blank=True)
    introduction = models.TextField(blank=True)
    projects_completed = models.IntegerField(blank=True)
    company_profile = models.FileField(upload_to='company_profiles/constructions/', blank=True)

class MaintainanceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True)
    portfolio = models.URLField(blank=True)
    introduction = models.TextField(blank=True)
    jobs_completed = models.IntegerField(blank=True)
    company_profile = models.FileField(upload_to='company_profiles/maintainances/', blank=True)

class SmartHomeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True)
    portfolio = models.URLField(blank=True)
    introduction = models.TextField(blank=True)
    projects_completed = models.IntegerField(blank=True)
    company_profile = models.FileField(upload_to='company_profiles/smart_home/', blank=True)


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

#----------------------------------------------------Start Projects Model-----------------------------------------------
class LandDetail(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="land_details")
    address = models.TextField()
    size_in_sq_ft = models.FloatField()
    survey_number = models.CharField(max_length=100, blank=True, null=True)
    building_type = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Land - {self.survey_number} (Customer: {self.customer.user.username})"
    

class Projects(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="projects")
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Pending')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    current_phase = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Project: {self.title} with {self.service_provider} (Status: {self.status})"
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def next_phase(self, phase_name):
        self.current_phase = phase_name
        self.save()


class Quotation(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='quotations')
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Quotation for {self.project.title} - Service Provider: {self.service_provider.username}"

#----------------------------------------------------End Projects Model-----------------------------------------------

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
    


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='messages/files/', blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"