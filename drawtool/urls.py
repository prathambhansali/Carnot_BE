"""AOI URL Configuration

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

from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('save_aoi/', views.save_aoi, name="save_aoi"),
    path('measure/<slug:proj_name>/<slug:date>', views.save_measure, name="save_measure"),
    path('get_data/<slug:proj_name>/<slug:date>', views.get_all_data_by_date, name="get_all_data_by_date"),
    path('delete/<int:id>/', views.delete_aoi, name="delete_aoi"),
]

# path('save/', views.save, name="save"),
# path('data/<int:projectId>/', views.get_all_data, name="get_all_data"),
# path('data/<int:projectId>/<slug:date>', views.get_all_data_by_date, name="get_all_data_by_date"),
# path('measure/', views.save_measurement, name="save"),
# path('measure/<int:projectId>/', views.get_all_measurement_data, name="get_all_data"),
# path('measure/<int:projectId>/<slug:date>', views.get_all_measurement_data_by_date, name="get_all_data_by_date"),
# path('delete/<int:id>/', views.delete_aoi, name="delete_aoi"),
# path('measure/delete/<int:id>/', views.delete_measure, name="delete_measure"),
