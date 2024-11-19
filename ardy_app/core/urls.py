# core/urls.py
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from knox import views as knox_views
from .views import LoginAPI, RegisterAPI

app_name = 'core'

urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterAPI.as_view(), name='register'),
    path('api/auth/login/', LoginAPI.as_view(), name='login'),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/auth/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('accounts/', include('allauth.urls')),
]