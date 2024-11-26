from django.contrib.sitemaps import Sitemap
from .models import *

class MainAnimationSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return MainAnimation.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class SloganSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return Slogan.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class WhyUsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return WhyUs.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class DiscoverUsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return DiscoverUs.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class HowItWorkSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return HowItWork.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class FAQSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return FAQ.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class SocialMediaSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return Social_Media.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class DownloadAppsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return DownloadApps.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class BusinessMainSectionSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return BusinessMainSection.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class BusinessSolutionsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return BusinessSolutions.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class BusinessStatisticsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return BusinessStatistics.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class BusinessRequestsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return BusinessRequests.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class BecomeaPartnerDescriptionSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return BecomeaPartnerDescription.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class BecomeaPartnerRequestsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return BecomeaPartnerRequests.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class CarearesDescriptionSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return CarearesDescription.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class CarearesRequestsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return CarearesRequests.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class ContactUsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return ContactUs.objects.all()
    def lastmod(self, obj):
        return obj.last_update


class PrivacySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    def items(self):
        return Privacy.objects.all()
    def lastmod(self, obj):
        return obj.last_update