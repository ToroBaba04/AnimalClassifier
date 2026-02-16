from django.urls import path
from . import views

app_name = 'classifier'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('verify-signup-2fa/', views.verify_signup_2fa, name='verify_signup_2fa'),
    path('login/', views.login_view, name='login'),
    path('verify-login-2fa/', views.verify_login_2fa, name='verify_login_2fa'),
    path('logout/', views.logout_view, name='logout'),
    
    # Classification URLs
    path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload'),
    path('history/', views.history, name='history'),
    path('statistics/', views.statistics, name='statistics'),
]
