from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime

#Users Imports
from django.contrib.auth.models import AbstractUser

# Create your models here.
SIGNUP_TYPE = [
    ("Manual", "Manual"),
    ("Google", "Google"),
    ("Apple", "Apple"),
]
class User(AbstractUser):
    USER_TYPES = [('Customer', 'Customer'), ('Consultant', 'Consultant'),
                ('Interior Designer', 'Interior Designer'), ('Construction', 'Construction'),
                ('Maintainance', 'Maintainance'),('Smart_Home', 'Smart_Home')]
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format : '+99999999999'. Up to 14 digits allowed.",)
    phone = models.CharField(validators=[phone_regex], max_length=14, blank=False, null=False, unique=True)

    # Default users fields.
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    news_letter = models.BooleanField(default=False)
    offers_and_discounts = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name=("date joined"), default=timezone.now)
    signup_type = models.CharField(default="Manual", max_length=6, choices=SIGNUP_TYPE, help_text='Type of Signup.')

    def update_date_field(self, new_date):
        new_date_obj = datetime.strptime(new_date, "%Y-%m-%d").date()
        self.birthday = new_date_obj
        self.save()
    
    # Seperate profiles for each user type
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    land_details = models.TextField(blank=True)
    property_type = models.CharField(max_length=100, blank=True)
    budget = models.IntegerField(blank=True)
    property_status = models.CharField(max_length=100, blank=True)
    project_details = models.TextField(blank=True)
    attachments = models.FileField(upload_to='customers/attachments',blank=True)

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