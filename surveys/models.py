
import os

import numpy as np
import pandas as pd

import random

from joblib import load
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from utils.models import (
    						Amenities,
							Property,
							Rooms ,
							Meals,
							Market,
							Distribution,
							Deposit,
							Customer,
							Hotels ,
       					)

from travel_recommender.settings import THRESHOLD_OF_BOOKING_PREDICTION, THRESHOLD_OF_ACCOMMODATE_PREDICTION



def get_required_columns(survey_object):
	return [ field.name for field in survey_object._meta.get_fields() if field.name not in ['id', 'user_id'] ]

def fill_constraints(object_models,is_select=False):
    
    constraints = []
    
    if is_select:
        constraints.append(('0', ''))
        
    for object_model in object_models.objects.all():
        constraints.append((str(object_model.type), object_model.label))
  
    return constraints


HOTELTYPES = fill_constraints(Hotels)
MEALTYPES = fill_constraints(Meals)
MARKET = fill_constraints(Market)
DISTRIBUTION = fill_constraints(Distribution)
DEPOSITTYPE = fill_constraints(Deposit)
CUSTOMERTYPE = fill_constraints(Customer)
ROOMTYPES = fill_constraints(Rooms, True)
PROPERTYTYPES = fill_constraints(Property, True)
AMENITIES = fill_constraints(Amenities)


class PersonalSurvey(models.Model):

	id = models.AutoField(unique=True, primary_key=True, auto_created=True, db_index=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+',null=True)
	lead_time = models.IntegerField( default=0)
	stays_in_weekend_nights  = models.IntegerField(default=0)
	stays_in_week_nights = models.IntegerField(default=0)
	adults = models.IntegerField(default=0)
	babies = models.IntegerField(default=0)
	children = models.IntegerField(default=0)
	booking_changes = models.IntegerField(default=0)
	days_in_waiting_list = models.IntegerField(default=0)
	adr = models.IntegerField(default=0)
	required_car_parking_spaces = models.IntegerField(default=0)
	total_of_special_requests = models.IntegerField(default=0)
	is_repeated_guest = models.IntegerField(default=0)
	hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE,related_name='+',null=True)
	meal = models.ForeignKey(Meals, on_delete=models.CASCADE,related_name='+',null=True)
	market_segment = models.ForeignKey(Market, on_delete=models.CASCADE,related_name='+',null=True)
	distribution_channel = models.ForeignKey(Distribution, on_delete=models.CASCADE,related_name='+',null=True)
	deposit_type = models.ForeignKey(Deposit, on_delete=models.CASCADE,related_name='+',null=True)
	customer_type = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='+',null=True)
 
	def insert_new_instance(self, user,
								hotel_type,
								meal_type,
								market_type,
								distribution_type,
								deposit,
								customer):
  
		new_personal_survey = PersonalSurvey.objects.create(
				user_id = User.objects.get(id = user),
				lead_time = self.lead_time,
				stays_in_weekend_nights = self.stays_in_weekend_nights,
				stays_in_week_nights = self.stays_in_week_nights,
				adults = self.adults,
				babies = self.babies,
				booking_changes = self.booking_changes,
				days_in_waiting_list = self.days_in_waiting_list,
				adr = self.adr,
				required_car_parking_spaces = self.required_car_parking_spaces,
				total_of_special_requests = self.total_of_special_requests,
				is_repeated_guest = self.is_repeated_guest,
				hotel = Hotels.objects.get(type = hotel_type),
				meal = Meals.objects.get(type = meal_type),
				market_segment = Market.objects.get(type = market_type),
				distribution_channel = Distribution.objects.get(type = distribution_type),
				deposit_type = Deposit.objects.get(type = deposit),
				customer_type = Customer.objects.get(type = customer)
			)
  
		return new_personal_survey
	

class AccommodateSurvey(models.Model):
	
	id = models.AutoField(unique=True, primary_key=True, auto_created=True, db_index=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+',null=True)
	host_total_listings_count = models.IntegerField(null=True)
	minimum_nights = models.IntegerField(null=True)
	maximum_nights = models.IntegerField(null=True)
	bedrooms = models.IntegerField(null=True)
	price = models.IntegerField(null=True)
	host_response_rate = models.FloatField(null=True)
	host_acceptance_rate = models.FloatField(null=True)
	property_type = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='+',null=True)
	room_type = models.ForeignKey(Rooms, on_delete=models.CASCADE,related_name='+',null=True)
	amenities = models.ManyToManyField(Amenities
                                    # through='AmenitySurveyGroups',
        							# through_fields=('survey_id', 'amenity_id'),
                                    #,related_name='+'
                                    )
	
	def get_values_for_data_frame(self):
		data_object = {
			"host_total_listings_count": self.host_total_listings_count,
			"minimum_nights": self.minimum_nights,
			"maximum_nights": self.maximum_nights,
			"bedrooms": self.bedrooms,
			"price": self.price,
			"host_response_rate": self.host_response_rate,
			"host_acceptance_rate": self.host_acceptance_rate,
			"property_type": self.property_type.label,
			"room_type": self.room_type.label,
   			"amenities": [ model_to_dict(amenity_object)['label'] for amenity_object in list(self.amenities.all())]
		}

		# for data_object in data_list:
		# 	data_object['amenities']
   
		return data_object
 
 
	def insert_new_instance(self, user,
								property,
								room,
								amenity_list):


		instance_accommodate_survey =  AccommodateSurvey.objects.create(
					user_id = User.objects.get(id = user),
					host_total_listings_count = self.host_total_listings_count,
					minimum_nights = self.minimum_nights,
					maximum_nights = self.maximum_nights,
					bedrooms = self.bedrooms,
					price = self.price,
					host_response_rate = self.host_response_rate,
					host_acceptance_rate = self.host_acceptance_rate,
					property_type = Property.objects.get(type = property),
					room_type = Rooms.objects.get(id = room)
     									)
     

		for amenity in amenity_list:
			amenity_instance = Amenities.objects.filter(type = amenity).first()
			instance_accommodate_survey.amenities.add(amenity_instance)
   
		return instance_accommodate_survey
	


class TripSurvey(models.Model):
	
	id = models.AutoField(unique=True, primary_key=True, auto_created=True, db_index=False)
	user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+',null=True)
	rate_of_religious_place = models.FloatField()
	rate_of_parks = models.FloatField()
	rate_of_theaters = models.FloatField()
	rate_of_mall = models.FloatField()
	rate_of_museum = models.FloatField()
	rate_of_art_gallery = models.FloatField()
	rate_of_zoo = models.FloatField()
	rate_of_restaurant = models.FloatField()
	rate_of_pubs = models.FloatField()
	rate_of_gym = models.FloatField()
	rate_of_spa = models.FloatField()
	rate_of_cafe = models.FloatField()
	rate_of_viewpoints = models.FloatField()
	rate_of_monument = models.FloatField(null=True)
 
	def insert_new_instance(self, user):

		new_trip_survey = TripSurvey.objects.create(
					user_id = User.objects.get(id = user),
     				rate_of_religious_place = self.rate_of_religious_place,
					rate_of_parks = self.rate_of_parks,
					rate_of_theaters = self.rate_of_theaters,
					rate_of_mall = self.rate_of_mall,
					rate_of_museum = self.rate_of_museum,
					rate_of_art_gallery = self.rate_of_art_gallery,
					rate_of_zoo = self.rate_of_zoo,
					rate_of_restaurant = self.rate_of_restaurant,
					rate_of_pubs = self.rate_of_pubs,
					rate_of_gym = self.rate_of_gym,
					rate_of_spa = self.rate_of_spa,
					rate_of_cafe = self.rate_of_cafe,
					rate_of_viewpoints = self.rate_of_viewpoints,
					rate_of_monument = self.rate_of_monument)
  
		return new_trip_survey



