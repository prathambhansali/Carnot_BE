from django.urls import path
from . import views

urlpatterns = [
    path('save_aoi/', views.save_aoi, name="save_aoi"),
    path('measure/<slug:proj_name>/<slug:date>',
         views.save_measure, name="save_measure"),
    path('get_data/<slug:proj_name>/<slug:date>',
         views.get_all_data_by_date, name="get_all_data_by_date"),
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
