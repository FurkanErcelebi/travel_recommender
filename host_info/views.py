import json
import random
from django.shortcuts import render
from .models import Host, HostRates
from .data_import import import_datas_to_host
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def transfer_infos_to_host(request):
    import_datas_to_host()
    return JsonResponse({'message': 'all datas are imported'})


@login_required
def view_hosts(request):
    return render(request=request, template_name='host_info/host_listing.html')


@csrf_exempt
def get_list_of_hosts(request):
    
    body_json = json.loads(request.body.decode())
    if 'keyword' in [ key for key in body_json.keys() ]:
        list_of_hosts = Host().search_hosts_by_name(body_json['keyword'] ,body_json['start_offset'], body_json['length'])
    else :
        list_of_hosts = Host().get_host_by_id_range(body_json['start_offset'], body_json['length']) 
                     
    for host_info in  list_of_hosts:
        host_info["url_page"] = f'/host_info/get-detail/{host_info["id"]}'

    return JsonResponse({'host_info_list': list_of_hosts})


@login_required
def get_detail_of_host(request, id):
    the_host = Host.objects.get(id= id)
    model_field_list = [ field for field in Host._meta.get_fields()]
    not_shown_fields = ['longitude', 'latitude', 'name','id', 'listing_id', 'host_id']
    the_host_details = [
        {
            "key": model_field.name.replace("_", " ") , 
            "value": the_host.get_amenities_in_array() if model_field.name == 'amenities' else the_host.property_type.label if model_field.name == 'property_type' else getattr(the_host, model_field.name)
        } for model_field in model_field_list if model_field.name not in not_shown_fields ]
    user_id = request.session['user_id']
    host_rate = HostRates().get_rate(user_id, id)
    context = {"the_host_details": the_host_details , "host_name": the_host.name, "host_rate": host_rate}
    return render(request = request,template_name='host_info/host_detailed_infos.html',context = context)


def get_all_rate_of_hosts(request):
    
    testList = []
    for i in range(15): 
        testList.append({'id': str(i), 'name': 'test{}'.format(i) , 'rate_score': random.randint(0,5)})
    
    json_data = {'all_host_rates': testList}  
    user_id = request.session['user_id']
    all_host_rates = HostRates().get_all_rates(user_id)
    json_data = { 'all_host_rates': all_host_rates }
    
    return JsonResponse(json_data)


@csrf_exempt
def set_rate_of_host(request):
    
    json_data = {}
    user_id = request.session['user_id']
        
    body_json = json.loads(request.body.decode())
    host_id = body_json['host_id']
    rate_score = body_json['rate_score']
    HostRates(rate_score = rate_score).give_rate(user_id=user_id, host_id=host_id)
    json_data = {'message': 'rating success full' }
    
    return JsonResponse(json_data)

