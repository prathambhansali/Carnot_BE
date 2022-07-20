from django.urls import re_path
from . import views

urlpatterns = [

    # url("check/(?P<project_name>[\w\ -]+)$", views.check, name="check"),
    re_path('upload/(?P<project_name>[\w\ -]+)$',
            views.upload, name="uploader"),
    re_path("store/(?P<project_name>[\w\ -]+)$",
            views.store_files_meta_info, name="meta_info"),

    # url("success/(?P<project_name>[\w\ -]+)/(?P<user_name>[\w\ -]+)$",views.completed_uploading,name="success_uploading"),

    # path("email/",views.get_email_users,name="user_emails"),
    # url("folder/(?P<project_name>[\w\ -]+)$",views.folder_finished,name="folder_finished"),
    # url('^get_cad_file/(?P<project_name>[\w\ -]+)$', views.cad_file, name="files"),
    # url('^get_3d_file/(?P<project_name>[\w\ -]+)$', views.three_d_file, name="files"),
    # url('^get_gcp_file/(?P<project_name>[\w\ -]+)$', views.gcp_file, name="files"),
]
