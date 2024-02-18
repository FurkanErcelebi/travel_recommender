import requests
import json
from math import radians, cos, sin, asin, sqrt
from travel_recommender.settings import API_KEY_FOR_MAPS, API_URL_FOR_MAPS, API_URL_FOR_PLACE, PLACE_URL


def get_trip_places(location: str, place_type):
    
    url = API_URL_FOR_MAPS.format(location, place_type,API_KEY_FOR_MAPS)

    locations = location.split(',')
    src_lat = float(locations[0])
    src_lng = float(locations[1])
    response = requests.request("GET", url, headers={}, data={})

    json_response = json.loads(response.text)
    results = json_response['results']
    
    last_results = []
    # print("==============")
    # print("founded places for place type {}".format(place_type))
    i = 0
    for result in results:
        lng = result['geometry']['location']['lng']
        lat = result['geometry']['location']['lat']
        distance = distance_between_locations(src_lat, lat, src_lng, lng)
        new_trip_place_info = {
            'place_name': result['name'],
            'place_id': result['place_id'],
            'place_types': result['types'],
            'place_longitude': result['geometry']['location']['lng'],
            'place_latitude': result['geometry']['location']['lat'],
            'google_maps_url': PLACE_URL.format(lat, lng),
            'distance': distance
        }
        # print("{} place name: {}".format(i, new_trip_place_info['place_name']))
        # print("{} place types: {}".format(i, new_trip_place_info['place_types']))
        # print("{} place longitude: {}".format(i, new_trip_place_info['place_longitude']))
        # print("{} place latitude: {}".format(i, new_trip_place_info['place_latitude']))
        # print("{} distance from source: {}".format(i, new_trip_place_info['distance']))
        # print("----------------")
        
        last_results.append(new_trip_place_info)
        i += 1
        
    # print("==============")
    
    return last_results


def get_photos_references(place_id):
    
    url = API_URL_FOR_PLACE.format(place_id, API_KEY_FOR_MAPS)
    
    response = requests.request("GET", url, headers={}, data={})
    
    result = {}
    if response.status_code == 200:
        json_response = json.loads(response.text)
        if json_response['status'] == 'OK' :
            result = json_response['result']
        else :
            print('Result is not ok with url and response: ',url , json_response)
    else : 
        print('Error occurred in api with url and response: ',url , response)
    
    photo_reference_list = []
    if 'photos' in result:
        for photo in result['photos']:
            photo_reference_list.append(photo['photo_reference'])
    
    return photo_reference_list

def get_ratings(place_id):
    url = API_URL_FOR_PLACE.format(place_id, API_KEY_FOR_MAPS)
    
    response = requests.request("GET", url, headers={}, data={})
    
    result = {}
    if response.status_code == 200:
        json_response = json.loads(response.text)
        if json_response['status'] == 'OK' :
            result = json_response['result']
        else :
            print('Result is not ok with url and response: ',url , json_response)
    else : 
        print('Error occurred in api with url and response: ',url , response)
    
    if 'rating' in result:
        return result['rating']
    else:
        return 0
    

def distance_between_locations(lat1, lat2, lon1, lon2):
	
	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	
	# calculate the result
	return(c * r)
	
	
def distance_between_trip_places(host_id):
    pass 

# # driver code
# lat1 = 53.32055555555556
# lat2 = 53.31861111111111
# lon1 = -1.7297222222222221
# lon2 = -1.6997222222222223
# print(distance(lat1, lat2, lon1, lon2), "K.M")

    
# {
# "html_attributions": [],
#   "results":
#     [
#       {
#         "business_status": "OPERATIONAL",
#         "geometry":
#           {
#             "location": { "lat": -33.8587323, "lng": 151.2100055 },
#             "viewport":
#               {
#                 "northeast":
#                   { "lat": -33.85739847010727, "lng": 151.2112436298927 },
#                 "southwest":
#                   { "lat": -33.86009812989271, "lng": 151.2085439701072 },
#               },
#           },
#         "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/bar-71.png",
#         "icon_background_color": "#FF9E67",
#         "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/bar_pinlet",
#         "name": "Cruise Bar",
#         "opening_hours": { "open_now": false },
#         "photos":
#           [
#             {
#               "height": 608,
#               "html_attributions":
#                 [
#                   '<a href="https://maps.google.com/maps/contrib/112582655193348962755">A Google User</a>',
#                 ],
#               "photo_reference": "Aap_uECvJIZuXT-uLDYm4DPbrV7gXVPeplbTWUgcOJ6rnfc4bUYCEAwPU_AmXGIaj0PDhWPbmrjQC8hhuXRJQjnA1-iREGEn7I0ZneHg5OP1mDT7lYVpa1hUPoz7cn8iCGBN9MynjOPSUe-UooRrFw2XEXOLgRJ-uKr6tGQUp77CWVocpcoG",
#               "width": 1080,
#             },
#           ],
#         "place_id": "ChIJi6C1MxquEmsR9-c-3O48ykI",
#         "plus_code":
#           {
#             "compound_code": "46R6+G2 The Rocks, New South Wales",
#             "global_code": "4RRH46R6+G2",
#           },
#         "price_level": 2,
#         "rating": 4,
#         "reference": "ChIJi6C1MxquEmsR9-c-3O48ykI",
#         "scope": "GOOGLE",
#         "types":
#           ["bar", "restaurant", "food", "point_of_interest", "establishment"],
#         "user_ratings_total": 1269,
#         "vicinity": "Level 1, 2 and 3, Overseas Passenger Terminal, Circular Quay W, The Rocks",
#       },
#       ...
#       ]
#     }