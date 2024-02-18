import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TipPlanRates, TripPlan

@csrf_exempt
def add_plan_to_calender(request):
    
    json_data = {}
    user_id = request.session['user_id']
    body_json = json.loads(request.body.decode())

    
    new_trip_plan = TripPlan(start_date = body_json['start_date'],
                            end_date = body_json['end_date'])
    
    previous_plans = new_trip_plan.is_plan_exist_in_specific_range()
    response = None
    if len(previous_plans) == 0:
        new_trip_plan.create_trip_plan(user_id = user_id, 
                                        host_id = body_json['host_id'],
                                        place_id_array = body_json['place_id_list'])
        json_data = {'message': 'plan inserted for user'}
        response = JsonResponse(json_data)
    else:
        response = JsonResponse({'message': 'theres is previous plan between these dates',
                                'start_date': previous_plans[0].start_date,
                                'end_date': previous_plans[0].end_date})
        response.status_code = 400
        
    return JsonResponse(json_data)


def get_plans_to_by_user_id(request):
    
    json_data = {}
    user_id = request.session['user_id']
    
    trip_plans = TripPlan().get_trip_plan_by_user_id(user_id)
    json_data = {'trip_plans': trip_plans}
        
    return JsonResponse(json_data)


@csrf_exempt
def remove_plan_from_calender(_, planid):
    
    json_data = {}
    TripPlan().delete_trip_plan(planid)
    json_data = {'message': 'plan deleted'}
        
    return JsonResponse(json_data)


def get_all_rate_of_trip_plans(request):
    
    testList = []
    for i in range(15): 
        testList.append({'id': str(i), 'name': 'test{}'.format(i) , 'rate_score': random.randint(0,5)})
    
    json_data = { 'all_trip_plan_rates': testList }
    user_id = request.session['user_id']
    all_trip_plan_rates = TipPlanRates().get_all_rates(user_id)
    json_data = { 'all_trip_plan_rates': all_trip_plan_rates }
    
    return JsonResponse(json_data)


@csrf_exempt
def give_rate_ro_trip_plan(request):
    
    json_data = {}
    user_id = request.session['user_id']
    body_json = json.loads(request.body.decode())
    
    plan_id = body_json['plan_id']
    rate_score = body_json['rate_score']
    TipPlanRates(rate_score = rate_score).give_rate(user_id=user_id, plan_id=plan_id)
    json_data = {'message': 'rating success full' }
    
    return JsonResponse(json_data)


