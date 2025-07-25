"""
URL configuration for telegram_django_auth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from telegram_django_auth.views import qr_login_view, change_language, telegram_view, phone_login_view, qr_wait_login, qr_password

urlpatterns = [
    path('', telegram_view, name='telegram'),
    path('qr/', qr_login_view, name='login-qr'),
    path('qr-wait-login/', qr_wait_login, name='login-qr-wait'),
    path('qr-password/', qr_password, name='login-qr-password'),
    path('admin/', admin.site.urls),
    path('phone/', phone_login_view, name='login-by-phone'),
    path('change-language/', change_language, name='change_language'),

    path("qr-code/", include("qr_code.urls", namespace="qr_code")),

]
