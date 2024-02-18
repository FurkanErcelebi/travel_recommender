
import os
from joblib import load
import numpy as np

from django.db import models
from django.db import connection
from django.forms.models import model_to_dict
import pandas as pd
#from django.contrib.gis.db import models as g_model
#from django.contrib.gis.db.models.functions import Distance
from host_info.models import Host
from .trip_planning import get_photos_references, get_ratings
from travel_recommender.settings import API_URL_FOR_PHOTOS, API_KEY_FOR_MAPS, API_URL_FOR_PLACE, PLACE_HOST_DISTANCE_LIMIT

# Create your models here.

distance_query = " ".join(["SELECT tp1.* , tp2.place_id", 
                           "FROM ( ",
						   "	SELECT (point(%s,%s) <@> point(tp.longitude,tp.latitude)) as distance , tp.* ",
						   "	FROM travel_search_tripplaces tp ",
						   "	ORDER BY distance ",
						   "	LIMIT %s ",
						   " ) tp1",
						   "INNER JOIN travel_search_tripplaces_place_type_id tp2 ON tp1.id = tp2.tripplaces_id",
						   "WHERE tp1.distance < %s; "]).replace("\t"," ")

class Place(models.Model):

	id = models.AutoField(unique=True, primary_key=True, auto_created=True, db_index=False)
	type = models.CharField(max_length=20)
	label = models.CharField(max_length=20)


class TripPlaces(models.Model):

	id = models.AutoField(unique=True, primary_key=True, auto_created=True, db_index=False)
	#place_type_id = models.ForeignKey(Place, on_delete=models.CASCADE,related_name='+')
	place_type_id = models.ManyToManyField(Place)
	google_maps_place_id = models.CharField(max_length=27, null=True)
	place_name = models.CharField(max_length=20)
	google_maps_url = models.URLField()
	longitude = models.FloatField()
	latitude = models.FloatField()

	def get_types_in_array(self):
		return [ place_type_info['label'] for place_type_info in list(self.place_type_id.all().values('label'))]
 
	def get_trip_place_by_id(self):
		trip_place = model_to_dict(TripPlaces.objects.get(id = self.id))
		the_trip_place = {}
		the_trip_place['place_name'] = trip_place['place_name']
		the_trip_place['google_maps_url'] = trip_place['google_maps_url']
		the_trip_place['place_type'] = model_to_dict(trip_place['place_type_id'][0])['label']
		return the_trip_place
 
	def set_trip_place(self, new_trip_place):
		
		the_trip_place = TripPlaces.objects.filter(google_maps_place_id__iexact = new_trip_place['place_id'])
		if len(the_trip_place) == 0:
			place_name = new_trip_place['place_name'];
			created_trip_place =  TripPlaces.objects.create(
														google_maps_place_id = new_trip_place['place_id'],
														google_maps_url = new_trip_place['google_maps_url'],
														longitude = new_trip_place['place_longitude'],
														latitude = new_trip_place['place_latitude'],
														place_name = place_name[0:20] 
              														if len(place_name) > 20 
                            										else place_name,
													)
   
			print(f"new trip place with id {created_trip_place.id}")
			the_trip_place = []
			the_trip_place.append(created_trip_place)
   

			the_place_type = None
			for founded_place_type in new_trip_place['place_types']:
				place_types = Place.objects.filter(type = founded_place_type)
				if(len(place_types) > 0) :
					the_place_type = place_types[0]
					the_trip_place[0].place_type_id.add(the_place_type)
    
    
	
	def get_nearest_trip_places_around_the_host(self,host_id, limit = 10):
		the_host = Host.objects.get(id = host_id)
		trip_places = None
		with connection.cursor() as cursor:
			cursor.execute(distance_query, [the_host.longitude, the_host.latitude, limit, PLACE_HOST_DISTANCE_LIMIT]) 
			trip_places = cursor.fetchall()
		return trip_places


	def get_nearest_trip_places(self, host_id, min = 5, max = 10):
  
		nearest_trip_places = self.get_nearest_trip_places_around_the_host(host_id,limit = max)

		trip_places = [
			{
				'id': nearest_trip_place[1],
				'distance': nearest_trip_place[0],
				'name': nearest_trip_place[2],
				'google_maps_url': nearest_trip_place[3],
				# look later for multiple types
				'place_type': Place.objects.filter(id=nearest_trip_place[7])[0].label,
				'photo_url_list': self.get_photo_urls(nearest_trip_place[6])
			}
			for nearest_trip_place in nearest_trip_places
		]
		
		return trip_places

	def get_photo_urls(self, place_id):
		photo_references_list = get_photos_references(place_id)
		photo_url_list = [ API_URL_FOR_PHOTOS.format(photo_references, API_KEY_FOR_MAPS) 
                    			for photo_references in photo_references_list]
		return photo_url_list

	def get_rating_and_types(self, place_id):
		rating = get_ratings(place_id)
		place_type_list = [place_type.label for place_type in TripPlaces.objects.get(google_maps_place_id = place_id).place_type_id.all()]
		return { 'rating': rating,
				 'types': place_type_list}
  
 		


