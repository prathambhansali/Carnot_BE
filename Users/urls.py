from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.home, name="login"),
    path('create/', views.create, name="create"),
    path('add_subuser/', views.add_subuser, name="add_subuser"),
    path('get_subuser/', views.get_subuser, name="get_subuser"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('generate_link/', views.generate_link, name="generate_link"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('verify_email/', views.verify_email, name="verify_email"),
]
