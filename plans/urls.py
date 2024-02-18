from django.urls import path

from . import views

app_name = "trip_plans"

urlpatterns = [
    path('add-plan-to-calender', views.add_plan_to_calender, name='addPlanToCalender'),
    path('get-plans', views.get_plans_to_by_user_id, name='getPlans'),
    path('remove-plan-from-calender/<int:planid>/', views.remove_plan_from_calender, name='removePlanFromCalender'),
    path('set-rate', views.give_rate_ro_trip_plan, name='setRate'),
    path('get-all-rates', views.get_all_rate_of_trip_plans, name='getAllRates')
]