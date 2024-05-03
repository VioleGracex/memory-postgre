"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import static

from django.conf import settings
from . import views

urlpatterns =i18n_patterns(
    path('admin/', admin.site.urls),
    path('admin', views.admin),
    path('', views.home, name='home'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('regpage/', views.regpage, name='regpage'),
    path('login/', views.login_user, name='login_user'),
    path('userfeed/', views.userfeed, name='userfeed'),
    path('profile/', views.profile, name='profile'),
    path('add_to_feed/', views.add_to_feed, name='add_to_feed'),
    path('myproject/', include('django.contrib.auth.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
)+ static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

