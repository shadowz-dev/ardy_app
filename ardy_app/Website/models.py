from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.urls import reverse
from ckeditor.fields import RichTextField
from ardy_app.settings import Base_URL
import random
import os

# Create your models here.

def upload_MainAnimation_image_path(instance, filename):
    new_filename = random.randint(1, 99966666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/MainAnimation/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class MainAnimation(models.Model):
    title = models.CharField(_("Title"),max_length=100, default=None)
    small_image = models.FileField(_("Small Image"),upload_to=upload_MainAnimation_image_path, default=None, null=True, blank=True)
    animate_image = models.FileField(_("Animate Image"),upload_to=upload_MainAnimation_image_path, default=None, null=True, blank=True)
    image = models.FileField(_("Image"),upload_to=upload_MainAnimation_image_path, default=None, null=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("Website:home")

class Slogan(models.Model):
    slogan = models.CharField(_("Slogan"), default=None, max_length=100)
    short_slogan = models.CharField(_("Short Slogan"), max_length=100, default=None)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slogan
    def get_absolute_url(self):
        return reverse("Website:home")
    
def upload_WhyUs_image_path(instance, filename):
    new_filename = random.randint(1, 99966666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/WhyUs/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class WhyUs(models.Model):
    image = models.FileField(_('Image'), upload_to=upload_WhyUs_image_path, default=None, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=100, default=None)
    description = models.TextField(_('Description'), default=None)
    last_update = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.slogan
    def get_absolute_url(self):
        return reverse("Website:home")
    
def upload_DiscoverUs_image_path(instance, filename):
    new_filename = random.randint(1, 99966666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/DiscoverUs/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class DiscoverUs(models.Model):
    title = models.CharField(_('Title'), max_length=100, default=None)
    sub_title = models.CharField(_('Sub Title'), max_length=100, default=None)
    description = models.TextField(_('Description'), default=None)
    image = models.FileField(_('Image'), upload_to=upload_DiscoverUs_image_path, default=None, null=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.slogan
    def get_absolute_url(self):
        return reverse("Website:home")
    
class HowItWork(models.Model):
    number = models.CharField(_("Number"), default=None, max_length=100)
    title = models.CharField(_("Title"), default=None, max_length=100)
    description = models.TextField(_("Description"), default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Home')
    

question = [
    ("General", "General"),
    ("Process", "Process"),
    ("Payments", "Payments"),
    ("Security", "Security"),
]
class FAQ(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    description = models.TextField(_("Description"), default=None)
    type = models.CharField(max_length=8, choices=question, default='General')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Home')
    
def upload_Social_Media_image_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/Social_Media/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class Social_Media(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    image = models.FileField(_("Image"), upload_to=upload_Social_Media_image_path, default=None, null=True, blank=True)
    link = models.URLField(_("Link"))
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Home')
    
def upload_DownloadApps_image_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/DownloadApps/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class DownloadApps(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    image = models.FileField(_("Image"), upload_to=upload_DownloadApps_image_path, default=None, null=True, blank=True)
    link = models.URLField(_("Link"))
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Home')
    
def upload_BusinessMainSection_image_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/BusinessMainSection/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class BusinessMainSection(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    logo = models.FileField(_("Logo"), upload_to=upload_BusinessMainSection_image_path, default=None, null=True, blank=True)
    description = models.TextField(_("Description"), default=None)
    link = models.URLField(_("Link"))
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Business')
    
def upload_BusinessSolutions_image_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/BusinessSolutions/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class BusinessSolutions(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    image = models.FileField(_("Image"), upload_to=upload_BusinessSolutions_image_path, default=None, null=True, blank=True)
    description = models.TextField(_("Description"), default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Business')
    
class BusinessStatistics(models.Model):
    number = models.CharField(_("Title"), default=None, max_length=100)
    description = models.TextField(_("Description"), default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number
    def get_absolute_url(self):
        return reverse('Website:Business')
    
class BusinessRequests(models.Model):
    company_name = models.CharField(_("Company Name"), max_length=255, default=None)
    your_name = models.CharField(_("Your Name"), unique=False, max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.")
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True, unique=False, default=None)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=False)
    description = models.TextField(_("Description"), blank=True, null=True)
    requested_at = models.DateTimeField(_("Requested At"), auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company_name)
    def get_absolute_url(self):
        return reverse('Website:Business')
    
class BecomeaPartnerDescription(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    description = models.TextField(_("Description"), default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Become_partner')
    
class BecomeaPartnerRequests(models.Model):
    restaurant_name = models.CharField(_("Restaurant Name"), max_length=255, default=None)
    your_name = models.CharField(_("Your Name"), unique=False, max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.")
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True, unique=False, default=None)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=False)
    requested_at = models.DateTimeField(_("Requested At"), auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.restaurant_name)
    def get_absolute_url(self):
        return reverse('Website:Become_partner')
    
#-----------------------------------------------Start CarearesDescription-----------------------------------------------
class CarearesDescription(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    description = models.TextField(_("Description"), default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Website:Careers')
#-------------------------------------------------End CarearesDescription-----------------------------------------------



#------------------------------------------------Start CarearesRequests-------------------------------------------------
def upload_Careares_Requests_Resumes_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/Careares_Requests_Resumes/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class CarearesRequests(models.Model):
    your_name = models.CharField(_("Your Name"), unique=False, max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.")
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True, unique=False, default=None)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=False)
    your_role = models.CharField(_("Your Role"), blank=True, null=True, unique=False, max_length=100)
    resume = models.FileField(_("Resume"), upload_to=upload_Careares_Requests_Resumes_path, default=None, null=True, blank=True)
    requested_at = models.DateTimeField(_("Requested At"), auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.your_name)
    def get_absolute_url(self):
        return reverse('Website:Careers')
# --------------------------------------------------End CarearesRequests------------------------------------------------



#------------------------------------------------Start Contact----------------------------------------------------------
def upload_Contact_images_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/Contact/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class ContactUs(models.Model):
    location = models.CharField(_("Location"), unique=False, max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.")
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True, unique=False, default=None)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=False)
    image = models.FileField(_("Image"), upload_to=upload_Contact_images_path, default=None, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.location)
    def get_absolute_url(self):
        return reverse('Website:Contact')
# --------------------------------------------------End Contact---------------------------------------------------------




#------------------------------------------------Start Privacy----------------------------------------------------------
class Privacy(models.Model):
    title = models.CharField(_("Title"), default=None, max_length=100)
    description = RichTextField(_("Description"), default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    def get_absolute_url(self):
        return reverse('Website:Privacy')
# --------------------------------------------------End Privacy---------------------------------------------------------




#-----------------------------------------------Start MetaTags----------------------------------------------------------
def upload_MetaTags_Images_path(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "website/MetaTags_Images/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class MetaTags(models.Model):
    PAGE_CHOICES = [
        ('Home', 'Home'),
        ('Business', 'Business'),
        ('Become', 'Become a partner'),
        ('Careers', 'Careers'),
        ('Contact', 'Contact us'),
        ('Privacy', 'Privacy'),
        ('Error', 'Error'),
    ]
    page_name = models.CharField(max_length=20, choices=PAGE_CHOICES, default='Home', help_text="Page name")
    title = models.CharField(max_length=255, help_text="Page title")
    description = models.TextField(help_text="Page description")
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords")
    author = models.CharField(max_length=255, blank=True, help_text="Author name")
    robots = models.CharField(max_length=255, default="index,follow", help_text="Robots instructions")
    language = models.CharField(max_length=7, default="en-US", help_text="Content language")
    viewport = models.CharField(max_length=255, default="width=device-width,initial-scale=1", help_text="Viewport settings")

    # Open Graph tags
    og_title = models.CharField(max_length=255, blank=True, help_text="Open Graph title")
    og_description = models.TextField(blank=True, help_text="Open Graph description")
    og_type = models.CharField(max_length=255, blank=True, help_text="Open Graph content type")
    og_url = models.URLField(blank=True, help_text="Open Graph URL")
    og_image = models.ImageField(blank=True, upload_to=upload_MetaTags_Images_path, help_text="Open Graph image")

    # Twitter Card tags
    twitter_card = models.CharField(max_length=255, blank=True, help_text="Twitter Card type")
    twitter_title = models.CharField(max_length=255, blank=True, help_text="Twitter Card title")
    twitter_description = models.TextField(blank=True, help_text="Twitter Card description")
    twitter_image = models.ImageField(blank=True, upload_to=upload_MetaTags_Images_path, help_text="Twitter Card image")

    # Additional tags (add as needed)
    apple_mobile_web_app_capable = models.CharField(max_length=255, blank=True, help_text="Apple mobile web app settings")
    theme_color = models.CharField(max_length=7, blank=True, help_text="Browser tab/toolbar color")
    msapplication_tap_highlight = models.CharField(max_length=255, default="#cccccc")

    use_facebook = models.BooleanField(default=False)
    facebook_app_id = models.CharField(max_length=255, blank=True, help_text="Facebook App ID")
    custom_namespace = models.CharField(max_length=255, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def get_meta_og_image(self):
        if self.og_image:
            return Base_URL + self.og_image.url
    def get_meta_twitter_image(self):
        if self.twitter_image:
            return Base_URL + self.twitter_image.url
    class Meta:
        verbose_name = 'Meta Tag'
        verbose_name_plural = 'Meta Tags'
#-------------------------------------------------End MetaTags----------------------------------------------------------
