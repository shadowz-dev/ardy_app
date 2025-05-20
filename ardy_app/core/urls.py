# core/urls.py
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from knox import views as knox_views
from core.views import *
from rest_framework.routers import DefaultRouter

app_name = 'core'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename='project')
router.register(r'phases', PhaseViewSet, basename='phase') # Consider nested under projects if desired
router.register(r'quotations', QuotationViewSet, basename='quotation')
router.register(r'drawings', DrawingViewSet, basename='drawing')
router.register(r'revisions', RevisionViewSet, basename='revision')
router.register(r'documents', DocumentViewSet, basename='document')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Authentication URLs
    path('api/auth/register/', RegisterAPIView.as_view(), name='knox_register'), # Use the new name
    path('api/auth/login/', LoginAPIView.as_view(), name='knox_login'),      # Use the new name
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    # Allauth URLs (if you are using it for social auth, password reset etc.)
    # path('accounts/', include('allauth.urls')), # Keep if used

    # Profile URLs (Example for retrieving/updating own profile)
    # Assumes your UserProfileView subclasses are named ...DetailView
    path('api/profiles/customer/', CustomerProfileDetailView.as_view(), name='customer-profile-detail'),
    path('api/profiles/consultant/', ConsultantProfileDetailView.as_view(), name='consultant-profile-detail'),
    path('api/profiles/interior/', InteriorProfileDetailView.as_view(), name='interior-profile-detail'),
    path('api/profiles/construction/', ConstructionProfileDetailView.as_view(), name='construction-profile-detail'),
    path('api/profiles/maintainance/', MaintenanceProfileDetailView.as_view(), name='maintainance-profile-detail'), # Check spelling
    path('api/profiles/smarthome/', SmartHomeProfileDetailView.as_view(), name='smarthome-profile-detail'),

    # Subscription URLs
    path('api/plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('api/subscribe/', SubscribeToPlanView.as_view(), name='subscribe'), # Corrected path for clarity
    path('api/promo/apply/', ApplySubPromoCodeView.as_view(), name='apply-promo'),

    # Referral URL
    path('api/referrals/', ReferralListView.as_view(), name='referral-list'),

    # Include router-generated URLs
    # This will create URLs like:
    # /api/projects/
    # /api/projects/{pk}/
    # /api/projects/{pk}/start/  (custom action)
    # etc. for all registered ViewSets
    path('api/', include(router.urls)),
]