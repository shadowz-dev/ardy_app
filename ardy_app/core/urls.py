# core/urls.py
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from knox import views as knox_views
from core.views import *

app_name = 'core'

urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterAPI.as_view(), name='register'),
    path('api/auth/login/', LoginAPI.as_view(), name='login'),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/auth/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('accounts/', include('allauth.urls')),
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('subscribe', SubscribeToPlanView.as_view(), name='subscribe'),
    path('promo/apply/', ApplySubPromoCodeView.as_view(), name='apply-promo'),
    path('referrals/', ReferralListView.as_view(), name='referral-list'),
    #----------------------------------Quotations URLS --------------------------------
    path('quotations/', QuotationListView.as_view(), name='quotations-list'),
    path('quotations/create/', QuotationCreateView.as_view(), name='quotations-create'),
    path('quotations/<int:pk>/update/', QuotationUpdateView.as_view(), name='quotations-update'),
    path('quotations/<int:pk>/approve/', QuotationApprovalView.as_view(), name='quotations-approve'),
    #----------------------------------End Quotations URLS --------------------------------
    #----------------------------------Drawings & Documents URLS --------------------------------
    path('drawings/', DrawingListView.as_view(), name='drawing-list'),
    path('drawings/upload/', DrawingUploadView.as_view(), name='drawing-upload'),
    path('revisions/request/', RevisionRequestView.as_view(), name='revision-request'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
]