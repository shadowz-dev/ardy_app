from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

app_name = 'Website'

sitemaps = {
    'mainanimation': MainAnimationSitemap,
    'slogan': SloganSitemap,
    'whybellmeals': WhyUsSitemap,
    'discoverbellmeals': DiscoverUsSitemap,
    'howitwork': HowItWorkSitemap,
    'questions': FAQSitemap,
    'socialmedia': SocialMediaSitemap,
    'downloadapps': DownloadAppsSitemap,
    'businessmainsection': BusinessMainSectionSitemap,
    'businesssolutions': BusinessSolutionsSitemap,
    'businessstatistics': BusinessStatisticsSitemap,
    'businessrequests': BusinessRequestsSitemap,
    'becomeapartnerdescription': BecomeaPartnerDescriptionSitemap,
    'becomeapartnerrequests': BecomeaPartnerRequestsSitemap,
    'carearesdescription': CarearesDescriptionSitemap,
    'carearesrequests': CarearesRequestsSitemap,
    'contactus': ContactUsSitemap,
    'privacy': PrivacySitemap,
}

urlpatterns = [
    # --------------------------------------------------Start Home------------------------------------------------------
    path('', Home, name='Home'),
    # ----------------------------------------------------Eng Home------------------------------------------------------
    # --------------------------------------------------Start Business--------------------------------------------------
    path('business', Business, name='Business'),
    # ----------------------------------------------------Eng Business--------------------------------------------------
    # --------------------------------------------------Start Become_partner--------------------------------------------
    path('partner', Become_partner, name='Become_partner'),
    # ----------------------------------------------------Eng Become_partner--------------------------------------------
    # --------------------------------------------------Start Careers---------------------------------------------------
    path('careers', Careers, name='Careers'),
    # ----------------------------------------------------Eng Careers---------------------------------------------------
    # --------------------------------------------------Start Contact---------------------------------------------------
    path('contact', Contact, name='Contact'),
    # ----------------------------------------------------Eng Contact---------------------------------------------------
    # --------------------------------------------------Start Privacy---------------------------------------------------
    path('privacy', Privacy_view, name='Privacy'),
    # ----------------------------------------------------Eng Privacy---------------------------------------------------
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]