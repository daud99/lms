"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('login/', views.login, name="login_login"),
    path('signup/', views.signup, name='signup'),
    # path('signup/', views.signuptest, name='signup'),
    path('dashboard/', include('dashboard.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout_logout"),
    path('accounts/', include('django.contrib.auth.urls')),

    # path('password_reset/', views.ResetPasswordRequestView.as_view(), name='reset_password'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done_lms'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm_lms'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete_lms'),
]
