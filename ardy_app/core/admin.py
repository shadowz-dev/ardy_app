from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User, CustomerProfile, ConsultantProfile, InteriorProfile, ConstructionProfile,
    MaintenanceProfile, SmartHomeProfile, CompanyProfile, EmployeeRelationship,
    UserOTP, SubscriptionPlan, UserSubscription, Referral, SubPromoCode, ServiceType,LandDetail, Projects,
    Phase, Quotation, Drawing, Revision, Document,
    Lead, Milestone, Review, FeaturedListing, EngagementLog, Transaction
)

class ServiceProviderProfileAdmin(admin.ModelAdmin): # A base admin for SP profiles
    list_display = ('user', 'company_name', 'expertise', 'experience')
    search_fields = ('user__username', 'company_name', 'expertise')
    autocomplete_fields = ['user']
    filter_horizontal = ('services_offered',) # Better UI for ManyToManyField
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'User'
    get_username.admin_order_field = 'user__username'
    
@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(ServiceProviderProfileAdmin): # Inherit common settings
    pass
@admin.register(InteriorProfile)
class InteriorProfileAdmin(ServiceProviderProfileAdmin):
    pass
@admin.register(ConstructionProfile)
class ConstructionProfileAdmin(ServiceProviderProfileAdmin):
    pass
@admin.register(MaintenanceProfile)
class MaintenanceProfileAdmin(ServiceProviderProfileAdmin):
    pass
@admin.register(SmartHomeProfile)
class SmartHomeProfileAdmin(ServiceProviderProfileAdmin):
    pass

# --- User and Profile Admin ---

class CustomerProfileInline(admin.StackedInline): # Or admin.TabularInline for more compact
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fk_name = 'user'
    fields = ('budget', 'property_status', 'project_details', 'attachments') # Explicitly list fields

class ConsultantProfileInline(admin.StackedInline): model = ConsultantProfile; can_delete=False; fk_name='user'; fields=('company_name', 'expertise', 'experience', 'portfolio', 'introduction', 'projects_completed', 'company_profile_doc', 'services_offered'); filter_horizontal=('services_offered',) # etc.
class InteriorProfileInline(admin.StackedInline): model = InteriorProfile; can_delete=False; fk_name='user'; fields=('company_name', 'expertise', 'experience', 'portfolio', 'introduction', 'projects_completed', 'company_profile_doc', 'services_offered'); filter_horizontal=('services_offered',)
class ConstructionProfileInline(admin.StackedInline): model = ConstructionProfile; can_delete=False; fk_name='user'; fields=('company_name', 'expertise', 'experience', 'portfolio', 'introduction', 'projects_completed', 'company_profile_doc', 'services_offered'); filter_horizontal=('services_offered',)
class MaintenanceProfileInline(admin.StackedInline): model = MaintenanceProfile; can_delete=False; fk_name='user'; fields=('company_name', 'expertise', 'experience', 'portfolio', 'introduction', 'projects_completed', 'company_profile_doc', 'services_offered'); filter_horizontal=('services_offered',)
class SmartHomeProfileInline(admin.StackedInline): model = SmartHomeProfile; can_delete=False; fk_name='user'; fields=('company_name', 'expertise', 'experience', 'portfolio', 'introduction', 'projects_completed', 'company_profile_doc', 'services_offered'); filter_horizontal=('services_offered',)


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    can_delete = False
    verbose_name_plural = 'Company Ownership'
    fk_name = 'owner' # Assuming 'owner' is the OneToOneField on CompanyProfile to User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Type & Phone', {'fields': ('user_type', 'phone')}),
        ('Marketing Preferences', {'fields': ('news_letter', 'offers_and_discounts')}),
        # ('Referral Info', {'fields': ('referred_by_user_link',)}) # If you add a display field
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'phone', 'email')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type', 'date_joined')
    list_filter = BaseUserAdmin.list_filter + ('user_type',)
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('username',)
    
    # Inlines for different profiles - only one will typically be relevant based on user_type
    # Consider conditional inlines if possible or just showing all (they'll be empty if not applicable)
    # A more advanced approach might use get_inlines based on user_type.
    inlines = [
        CustomerProfileInline, ConsultantProfileInline, InteriorProfileInline,
        ConstructionProfileInline, MaintenanceProfileInline, SmartHomeProfileInline,
        CompanyProfileInline # If a user can be a company owner
    ]

    # If you want to easily see who referred this user:
    # readonly_fields = ('referred_by_user_link',)
    # def referred_by_user_link(self, obj):
    #     if hasattr(obj, 'referred_by') and obj.referred_by:
    #         link = reverse("admin:core_user_change", args=[obj.referred_by.referrer.id])
    #         return format_html('<a href="{}">{}</a>', link, obj.referred_by.referrer.username)
    #     return "N/A"
    # referred_by_user_link.short_description = 'Referred By'


# Explicitly register Profile models if you want them to have their own admin pages
# (useful if they have many fields or you don't want them only as inlines)
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget', 'property_status')
    search_fields = ('user__username', 'user__email', 'project_details')
    autocomplete_fields = ['user']

# Do similar for ConsultantProfile, InteriorProfile, etc. if desired
# Register concrete profiles using the base ServiceProviderProfileAdmin


class EmployeeRelationshipInline(admin.TabularInline):
    model = EmployeeRelationship
    fk_name = 'company'
    extra = 1
    autocomplete_fields = ['employee']

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'owner', 'created_at')
    search_fields = ('company_name', 'owner__username')
    inlines = [EmployeeRelationshipInline]
    autocomplete_fields = ['owner']

@admin.register(EmployeeRelationship)
class EmployeeRelationshipAdmin(admin.ModelAdmin):
    list_display = ('company', 'get_employee_username', 'job_title', 'start_date')
    list_filter = ('company__company_name',)
    search_fields = ('company__company_name', 'employee__username', 'job_title')
    autocomplete_fields = ['company', 'employee']
    
    def get_employee_username(self, obj):
        return obj.employee.username
    get_employee_username.short_description = 'Employee'
    get_employee_username.admin_order_field = 'employee__username'

@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'otp_type_display', 'count_display')
    list_filter = ('otp_type',)
    search_fields = ('user__username', 'phone', 'email')
    
    def otp_type_display(self, obj):
        return obj.get_otp_type_display()
    otp_type_display.short_description = 'OTP Type'
    
    def count_display(self, obj):
        return obj.count
    count_display.short_description = 'OTP Sent Count'


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'category_display', 'default_order', 'is_standard_phase_service')
    list_filter = ('category', 'is_standard_phase_service')
    search_fields = ('name', 'description')
    list_editable = ('default_order', 'is_standard_phase_service', 'category')
    ordering = ('default_order', 'name')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'category')}),
        ('Standard Phase Configuration', {
            'fields': ('is_standard_phase_service', 'default_order', 
                        'default_phase_title_template', 'default_phase_description_template'),
            'description': "Configure if this service type is part of the default project phase setup and its order/templates."
        }),
    )
    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Category'
    
# --- Subscription Admin ---
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_type_display_custom', 'price', 'is_active', 'is_default_free_plan')
    list_filter = ('user_type', 'is_active', 'is_default_free_plan')
    search_fields = ('name',)
    list_editable = ('is_default_free_plan',)

    def get_user_type_display_custom(self, obj): # Custom method because original might not exist directly on model
        return dict(obj._meta.get_field('user_type').choices).get(obj.user_type)
    get_user_type_display_custom.short_description = 'Plan For'

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan__name')
    search_fields = ('user__username', 'plan__name')
    autocomplete_fields = ['user', 'plan']
    date_hierarchy = 'start_date'

# --- Referral & PromoCode Admin ---
@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'code', 'reward', 'is_redeemed')
    list_filter = ('is_redeemed',)
    search_fields = ('referrer__username', 'referred_user__username', 'code')
    autocomplete_fields = ['referrer', 'referred_user']

@admin.register(SubPromoCode)
class SubPromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'max_uses', 'uses', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active',)
    search_fields = ('code',)
    readonly_fields = ('uses',)


# --- Project Workflow Admin ---

@admin.register(LandDetail)
class LandDetailAdmin(admin.ModelAdmin):
    list_display = ('customer', 'location', 'land_area_in_sq_ft', 'building_type', 'is_approved')
    list_filter = ('building_type', 'is_approved')
    search_fields = ('customer__user__username', 'location', 'survey_number')
    autocomplete_fields = ['customer']

class PhaseInline(admin.TabularInline): # Or StackedInline
    model = Phase
    extra = 1
    fields = ('title', 'order', 'service_provider', 'status', 'start_date', 'expected_end_date', 'actual_end_date')
    ordering = ('order',)
    autocomplete_fields = ['service_provider']

class QuotationInline(admin.TabularInline):
    model = Quotation
    extra = 0
    fields = ('phase', 'service_provider', 'type', 'amount', 'status', 'submitted_at')
    readonly_fields = ('submitted_at',)
    autocomplete_fields = ['phase', 'service_provider']

class DrawingInline(admin.TabularInline):
    model = Drawing
    extra = 0
    fields = ('phase', 'uploaded_by', 'title', 'version', 'file', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['phase', 'uploaded_by']

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ('phase', 'uploaded_by', 'title', 'file', 'description', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    autocomplete_fields = ['phase', 'uploaded_by']


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'status', 'active_phase_display', 'start_date', 'expected_end_date')
    list_filter = ('status', 'customer__user__user_type')
    search_fields = ('title', 'customer__user__username', 'description')
    ordering = ('-start_date',)
    inlines = [PhaseInline, QuotationInline, DrawingInline, DocumentInline]
    readonly_fields = ('start_date', 'actual_end_date') # These are often system-set
    autocomplete_fields = ['customer', 'land_detail', 'active_phase']

    def active_phase_display(self, obj):
        return obj.active_phase.title if obj.active_phase else "N/A"
    active_phase_display.short_description = 'Active Phase'

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_link', 'required_service_type', 'service_provider', 'order', 'status', 'start_date')
    list_filter = ('status', 'required_service_type', 'project__customer__user__user_type', 'service_provider__user_type')
    search_fields = ('title', 'project__title', 'service_provider__username', 'description')
    ordering = ('project', 'order')
    autocomplete_fields = ['project', 'service_provider', 'required_service_type'] # Add required_service_type
    readonly_fields = ('actual_end_date',)
    filter_horizontal = ('customer_attachements',) # If you want a nicer M2M widget

    def project_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        link = reverse("admin:core_projects_change", args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', link, obj.project.title)
    project_link.short_description = 'Project'


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_link', 'phase', 'service_provider', 'type', 'amount', 'status', 'submitted_at')
    list_filter = ('status', 'type', 'service_provider__user_type')
    search_fields = ('project__title', 'service_provider__username', 'details')
    readonly_fields = ('submitted_at', 'updated_at', 'approved_at')
    autocomplete_fields = ['project', 'phase', 'service_provider']

    def project_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        link = reverse("admin:core_projects_change", args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', link, obj.project.title)
    project_link.short_description = 'Project'

@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_link', 'phase', 'version', 'uploaded_by', 'created_at')
    list_filter = ('project__customer__user__user_type', 'phase')
    search_fields = ('title', 'project__title', 'uploaded_by__username', 'notes')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['project', 'phase', 'uploaded_by'] # Or uploaded_by_consultant

    def project_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        link = reverse("admin:core_projects_change", args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', link, obj.project.title)
    project_link.short_description = 'Project'

@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ('drawing_link', 'customer', 'requested_at', 'resolved')
    list_filter = ('resolved',)
    search_fields = ('drawing__title', 'customer__user__username', 'comment')
    readonly_fields = ('requested_at', 'resolved_at')
    autocomplete_fields = ['drawing', 'customer']

    def drawing_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        link = reverse("admin:core_drawing_change", args=[obj.drawing.id])
        return format_html('<a href="{}">Drawing ID: {} (v{})</a>', link, obj.drawing.id, obj.drawing.version)
    drawing_link.short_description = 'Drawing'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title_display', 'project_link', 'phase', 'uploaded_by', 'uploaded_at')
    list_filter = ('project__customer__user__user_type', 'phase')
    search_fields = ('title', 'description', 'project__title', 'uploaded_by__username')
    readonly_fields = ('uploaded_at',)
    autocomplete_fields = ['project', 'phase', 'uploaded_by']

    def project_link(self, obj):
        if obj.project:
            from django.urls import reverse
            from django.utils.html import format_html
            link = reverse("admin:core_projects_change", args=[obj.project.id])
            return format_html('<a href="{}">{}</a>', link, obj.project.title)
        return "N/A"
    project_link.short_description = 'Project'

    def title_display(self, obj):
        return obj.title or obj.file.name.split('/')[-1]
    title_display.short_description = 'Title/Filename'
    

# Register other models if they exist and you want to manage them
admin.site.register(Lead)
admin.site.register(Milestone)
admin.site.register(Review)
admin.site.register(FeaturedListing)
admin.site.register(EngagementLog)
admin.site.register(Transaction)

    
