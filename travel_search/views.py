import json
import datetime
import random as rand

from dateutil import parser
from .trip_planning import get_trip_places
from .models import Place, TripPlaces
from django.shortcuts import render
from plans.models import TripPlan
from host_info.models import Host
from plans.evaluator import Evaluator

from travel_recommender.settings import NUMBER_OF_PLANS_EVERY_TURN
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
from faker import Faker

faker = Faker()
place_types = [ place.label for place in Place.objects.all() ]

# Create your views here.

@login_required
def view_rcm_plans(request):
    return render (request=request, template_name="travel_search/travel_search_plans_list.html")

def getRandomRange(number_of_places):
    
    currentDay = datetime.date.today().day
    start_day = currentDay + rand.randint(2, 30)
    is_next_mount = 1 if start_day > 30 else 0 
    start_day = start_day % 30
    start_day = 1 if start_day == 0 else start_day
    start_day = '0{0}'.format(start_day) if start_day < 10 else '{0}'.format(start_day) 
    currentMonth = datetime.date.today().month
    start_month = rand.randint(currentMonth, currentMonth + 4) + is_next_mount
    is_next_year = 1 if start_month > 12 else 0 
    start_month = start_month % 12
    start_month = '0{0}'.format(start_month) if start_month < 10 else '{0}'.format(start_month) 
    currentYear = datetime.date.today().year
    start_year = currentYear + is_next_year
    start_date = '{0}-{1}-{2}'.format(start_year, start_month, start_day);
    
    date_format = "%Y-%m-%d"
    formatted_start_date = datetime.datetime.strptime(start_date, date_format)
    
    formatted_end_date = formatted_start_date + datetime.timedelta(days=number_of_places)
    
    end_date = '{0}-{1}-{2}'.format(formatted_end_date.year, formatted_end_date.month, formatted_end_date.day)
    
    return [start_date, end_date]


def get_rcm_plans(request):
    """
        main recommender endpoint
    """
        
    get_hosts_randomly = True
    get_plan_randomly = True
    prices = []
    
    evaluator = Evaluator()
    evaluator.set_user_id(request.session['user_id'])
    # evaluator.set_user_id(request.GET.get('user_id'))
    evaluator.is_suitable_for_finding_trip_plan()

    if evaluator.get_is_suitable():
        print("USER DEMAND FROM PERSONAL SURVEY IS SUITABLE")
        evaluator.get_appropriate_accommodate_places()
        recommended_host_infos = evaluator.get_recommended_host_infos()
        
        get_hosts_randomly = not recommended_host_infos['result']
        if not get_hosts_randomly :
            print("USER DEMAND FROM ACCOMMODATE SURVEY IS SUITABLE")
            prices = [ int(one_price) for one_price in  recommended_host_infos['price_range'].split('-')]
            evaluator.get_cluster_of_trip_place_around_by_user()
        else:
            print("USER DEMAND FROM ACCOMMODATE SURVEY NOT FOUND AS SUITABLE")
            
    else :
        print("USER DEMAND FROM PERSONAL SURVEY NOT FOUND AS SUITABLE")


    have_all_plans = False
    hosts_and_trip_places = []
    
    while not have_all_plans:
        
        if get_hosts_randomly :
            list_of_hosts = Host().get_name_price_property_type_randomly(number=NUMBER_OF_PLANS_EVERY_TURN)
        else :
            list_of_hosts = Host().get_name_price_property_type_randomly_in_price_range(
                                                            prices[0], prices[1], number=NUMBER_OF_PLANS_EVERY_TURN)
        
        for host in list_of_hosts :
            
            get_plan_randomly = True
            if not get_hosts_randomly:
                evaluator.get_cluster_of_host_by_place_types(host_id=host['id'])
                if evaluator.is_user_and_host_cluster_matching():
                    print("USER DEMAND FROM TRIP PLACE SURVEY IS SUITABLE AND A PLAN CREATING...")
                    nearest_trip_place_list = evaluator.get_formatted_trip_places()
                    random_date_interval = getRandomRange(len(nearest_trip_place_list))
                    hosts_and_trip_places.append({
                        "host_infos": host,
                        "host_url": Host(id=host['id']).get_host_url(),
                        "start_date": random_date_interval[0],
                        "end_date": random_date_interval[1],
                        "trip_places": nearest_trip_place_list
                    })
                    get_plan_randomly = False
                else:
                    print("USER DEMAND FROM TRIP PLACE SURVEY NOT FOUND AS SUITABLE")
                    
            
            if get_plan_randomly :
                # print("USER DEMAND FROM TRIP PLACE SURVEY NOT FOUND AS SUITABLE")
                nearest_trip_place_list = TripPlaces().get_nearest_trip_places(host_id=host['id']) 
                if len(nearest_trip_place_list) > 0 :
                    
                    random_date_interval = getRandomRange(len(nearest_trip_place_list))
                    hosts_and_trip_places.append({
                        "host_infos": host,
                        "host_url": Host(id=host['id']).get_host_url(),
                        "start_date": random_date_interval[0],
                        "end_date": random_date_interval[1],
                        "trip_places": nearest_trip_place_list
                    })
                
        
        if len(hosts_and_trip_places) >= NUMBER_OF_PLANS_EVERY_TURN :
            have_all_plans = True
 
    hosts_and_trip_places = hosts_and_trip_places[0: NUMBER_OF_PLANS_EVERY_TURN]
    
    return JsonResponse({'hosts_and_trip_places': hosts_and_trip_places})
    



def get_photo_urls_from_place_id(request):
    place_id = request.GET.get('place_id')
    photo_url_list = TripPlaces().get_photo_urls(place_id)
    return JsonResponse({'photo_urls': photo_url_list})

def set_trip_places_near_for_every_hosts(start_offset, length):
    
    i = start_offset
    list_of_hosts = Host().get_coordinates_by_id_range(start_offset, length)
    for the_host in list_of_hosts:
        
        location =  f"{the_host['latitude']} , {the_host['longitude']}"
        
        all_trip_places = []
    
        for place_type in place_types:
            trip_places = get_trip_places(location=location, place_type=place_type)
            all_trip_places.extend(trip_places)
            
        for trip_places in all_trip_places:
            TripPlaces().set_trip_place(trip_places)
        
        print("host with id {0} in row {1} have related place infos in database".format(the_host['id'], i));
        i = i + 1

@csrf_exempt
def get_host_and_ist_surroundings_trip_places(request):
    
    body_json = json.loads(request.body.decode())
    
    set_trip_places_near_for_every_hosts(body_json['start_offset'],body_json['length'])
    
    
    return JsonResponse({'message': "all trip places added to database table"})
    
