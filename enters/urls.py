from django.urls import path

from . import views

app_name = "enters"

urlpatterns = [
    path('signup', views.sign_up_view, name='signup'),
    path('success', views.success_message_view, name='succesfull-signup'),
	path('<int:uid>/',views.validate_user, name='validation'),
	path('login',views.login_view, name='login'),
	path('postEnter',views.post_first_login_view, name='postEnter'),
	path('logout',views.logout_user, name='logout'),
]