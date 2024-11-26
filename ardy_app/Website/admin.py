
from django.contrib import admin
from .models import *

@admin.register(MainAnimation)
class MainAnimationAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Slogan)
class SloganAdmin(admin.ModelAdmin):
    list_display = ('slogan', 'short_words')

@admin.register(WhyUs)
class WhyBellMealsAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(DiscoverUs)
class DiscoverBellMealsAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(HowItWork)
class HowItWorkAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(FAQ)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')

@admin.register(Social_Media)
class Social_MediaAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(DownloadApps)
class DownloadAppsAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(BusinessMainSection)
class BusinessMainSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(BusinessSolutions)
class BusinessSolutionsAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(BusinessStatistics)
class BusinessStatisticsAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(BusinessRequests)
class BusinessRequestsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'your_name', 'phone', 'email', 'requested_at')



@admin.register(BecomeaPartnerDescription)
class BecomeaPartnerDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(BecomeaPartnerRequests)
class BecomeaPartnerRequestsAdmin(admin.ModelAdmin):
    list_display = ('restaurant_name', 'requested_at')

@admin.register(CarearesDescription)
class CarearesDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(CarearesRequests)
class CarearesRequestsAdmin(admin.ModelAdmin):
    list_display = ('your_name', 'requested_at')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('location',)

@admin.register(Privacy)
class PrivacyAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(MetaTags)
class MetaTagsAdmin(admin.ModelAdmin):
    list_display = ('title',)