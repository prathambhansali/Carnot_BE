"""folders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [

    # url("check/(?P<project_name>[\w\ -]+)$", views.check, name="check"),
    url('upload/(?P<project_name>[\w\ -]+)$',views.upload,name="uploader"),
    url("store/(?P<project_name>[\w\ -]+)$",views.store_files_meta_info,name="meta_info"),

    # url("success/(?P<project_name>[\w\ -]+)/(?P<user_name>[\w\ -]+)$",views.completed_uploading,name="success_uploading"),

    # path("email/",views.get_email_users,name="user_emails"),
    # url("folder/(?P<project_name>[\w\ -]+)$",views.folder_finished,name="folder_finished"),
    # url('^get_cad_file/(?P<project_name>[\w\ -]+)$', views.cad_file, name="files"),
    # url('^get_3d_file/(?P<project_name>[\w\ -]+)$', views.three_d_file, name="files"),
    # url('^get_gcp_file/(?P<project_name>[\w\ -]+)$', views.gcp_file, name="files"),
]

