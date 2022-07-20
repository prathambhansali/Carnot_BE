from django.urls import path
from carnot_backend import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.home, name="login"),
    path('create/', views.create, name="create"),
    path('add_subuser/', views.add_subuser, name="add_subuser"),
    path('get_subuser/', views.get_subuser, name="get_subuser"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('generate_link/', views.generate_link, name="generate_link"),
    path('reset_password/', views.reset_password, name="reset_password"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
