from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "host_info"

urlpatterns = [
    path('transfer-data', views.transfer_infos_to_host, name='transferDatas'),
    path('get-list', views.get_list_of_hosts, name='getList'),
    path('list', views.view_hosts, name='setView'),
    path('get-detail/<int:id>', views.get_detail_of_host, name='getDetail'),
    path('set-rate', views.set_rate_of_host, name='setRate'),
    path('get-all-rates', views.get_all_rate_of_hosts, name='getAllRates')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)