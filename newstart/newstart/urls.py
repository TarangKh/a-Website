"""
URL configuration for newstart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from home.views import *
from crud.views import *

urlpatterns = [
    path("delete-account/", del_account, name="del_account"),
    path("user-smash/<int:id>", smash_user, name="smash_user"),
    path("user-pass/<int:id>", pass_user, name="pass_user"),
    path("update-profile/", update_page, name="update_page"),
    path("logout/", logout_page, name="logout_page"),
    path("login/", login_page, name="login_page"),
    path("register/user-info/", register_info, name="register_info"),
    path("", register_auth, name="register_auth"),
    path("profile-page/", profile_page, name = "profile_page"),
]
