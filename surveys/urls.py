from django.urls import path

from . import views

app_name = "surveys"

urlpatterns = [
    path('new-personal-survey', views.personal_survey_view, name='newPersonalSurvey'),
    path('new-accommodate-survey', views.accommodate_survey_view, name='newAccommodateSurvey'),
    path('new-trip-survey', views.trip_survey_view, name='newTripSurvey')
]