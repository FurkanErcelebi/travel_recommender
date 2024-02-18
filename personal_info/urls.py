from django.urls import path

from . import views

app_name = "person"

urlpatterns = [
    path('edit-info', views.view_personal_infos, name='personInfoEnter'),
    path('account', views.view_personal_dashboard, name='personDashboard'),
    path('settings', views.view_personal_settings, name='personSettings'),
    path('survey-infos', views.view_survey_infos, name='personSurveyInfos'),
    path('get-survey-responses', views.get_survey_infos, name='personSurveyResponses'),
    path('new-survey-responses', views.edit_survey_infos, name='personNewSurveyResponses'),
    path('new-personal-info', views.edit_personal_infos, name='personInfoResponses'),
    path('calender', views.view_and_edit_travel_calender, name='personCalender')
]