from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('rcm_plans/', include('travel_search.urls')),
    path('trip_plans/', include('plans.urls')),
    path('host_info/', include('host_info.urls')),
    path('survey/', include('surveys.urls')),
    path('personal_info/', include('personal_info.urls')),
    path('register/', include('enters.urls')),
    path('admin/', admin.site.urls),
]