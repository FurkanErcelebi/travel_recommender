from django.urls import path

from . import views

app_name = "travel_search"

urlpatterns = [
    path('', views.view_rcm_plans, name='planListing'),
    path('set-all-host-trip-plan', views.get_host_and_ist_surroundings_trip_places, name='hostPlaces'),
    path('get-host-trip-plan', views.get_rcm_plans, name='hostPlaceList'),
    path('get-photo-urls', views.get_photo_urls_from_place_id, name='getPhotoUrls')
]