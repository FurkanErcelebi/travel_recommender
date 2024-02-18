

import collections
import os
import numpy as np
import pandas as pd

from django.contrib.auth.models import User
from host_info.models import HostRates
from plans.models import TipPlanRates
from surveys.models import AccommodateSurvey, PersonalSurvey, TripSurvey
from travel_recommender.settings import THRESHOLD_OF_ACCOMMODATE_PREDICTION, THRESHOLD_OF_BOOKING_PREDICTION
from travel_search.models import Place, TripPlaces
from utils.models import Customer, Deposit, Distribution, Hotels, Market, Meals, Property, Rooms
from joblib import load


class Evaluator():
	
    user_id = ''
    is_suitable = False
    recommended_host_infos = { 'result': False, 'price_range': [] }
    place_types = [ place.label for place in Place.objects.all()]
    price_list = []
    user_clusters = []
    host_cluster = ''
    survey_infos = []
    foreign_columns = []
    required_columns = []
    required_properties = []
    nearest_trip_places = []
    dataset = {}
    evaluator = object
    normalizer = object
    normalizer2 = object
    
    def set_user_id(self, user_id):
        self.user_id = user_id
    
    def get_user(self):
        return User.objects.get(id = self.user_id)
    
    def get_is_suitable(self):
        return self.is_suitable
    
    def get_recommended_host_infos(self):
        return self.recommended_host_infos
    
    def is_user_and_host_cluster_matching(self):
        return len(self.nearest_trip_places) > 0 and self.host_cluster in  self.user_clusters
    
    def get_formatted_trip_places(self):
        
        formatted_trip_places = [
			{
				'id': nearest_trip_place[1],
				'distance': nearest_trip_place[0],
				'name': nearest_trip_place[2],
				'google_maps_url': nearest_trip_place[3],
				# look later for multiple types
				'place_type': Place.objects.filter(id=nearest_trip_place[7])[0].label,
				'photo_url_list': TripPlaces().get_photo_urls(nearest_trip_place[6])
			}
			for nearest_trip_place in self.nearest_trip_places
		]
        return formatted_trip_places
    
    def convert_list_to_data_frame_from_personal_survey_infos(self):
		
        data_frame = {}

        for required_field in self.required_columns:
            data_frame[required_field] = []
   
        for val in self.survey_infos:
            for required_field in self.required_columns:
                if len(self.foreign_columns) > 0 and required_field in self.foreign_columns:
                    if required_field == 'hotel':
                        data_frame[required_field].append(Hotels.objects.get(id = val['{}_id'.format(required_field)]).label)
                    elif required_field == 'meal':
                        data_frame[required_field].append(Meals.objects.get(id = val['{}_id'.format(required_field)]).label)
                    elif required_field == 'market_segment':
                        data_frame[required_field].append(Market.objects.get(id = val['{}_id'.format(required_field)]).label)
                    elif required_field == 'distribution_channel':
                        data_frame[required_field].append(Distribution.objects.get(id = val['{}_id'.format(required_field)]).label)
                    elif required_field == 'deposit_type':
                        data_frame[required_field].append(Deposit.objects.get(id = val['{}_id'.format(required_field)]).label)
                    elif required_field == 'customer_type':
                        data_frame[required_field].append(Customer.objects.get(id = val['{}_id'.format(required_field)]).label)
                else:
                    data_frame[required_field].append(val[required_field])

        return data_frame
		
  
    def is_suitable_for_finding_trip_plan(self):
        """
			Find  class value to make
			sure it is wort to do recommending
  			"""

        self.foreign_columns = ['hotel','meal','market_segment','distribution_channel','deposit_type','customer_type']
        self.required_columns = [
			 				'hotel'               
 							,'lead_time'                   
 							,'stays_in_weekend_nights'     
 							,'stays_in_week_nights'
 							,'adults'                      
 							,'children'                    
 							,'babies'                      
 							,'meal'                        
 							,'market_segment'              
 							,'distribution_channel'        
 							,'is_repeated_guest'           
 							,'booking_changes'             
 							,'deposit_type'                
 							,'days_in_waiting_list'        
 							,'customer_type'               
 							,'adr'                         
 							,'required_car_parking_spaces' 
 							,'total_of_special_requests']
        

        user = self.get_user()
        self.survey_infos =  list(PersonalSurvey.objects.filter(user_id = user).values())
        if len(self.survey_infos) > 1 and len(self.survey_infos) % 2 == 0:
            self.survey_infos.pop()
        data_frame = self.convert_list_to_data_frame_from_personal_survey_infos()
        self.dataset = pd.DataFrame(data_frame)
        dataset_encoded = self.dataset.copy()
        for foreign_field in self.foreign_columns:
            labeler = load('{0}/static/surveys/models/personal/labeler_for_{1}.joblib'.format(
                                    os.getcwd().replace('\\', '/'), foreign_field))
            dataset_encoded[foreign_field] = labeler.transform(self.dataset[foreign_field])
        
        self.normalizer = load('{}/static/surveys/models/personal/normalizer.joblib'.format(os.getcwd().replace('\\', '/')))
        dataset_encoded = self.normalizer.transform(dataset_encoded)
        self.evaluator = load('{}/static/surveys/models/personal/evaluator.joblib'.format(os.getcwd().replace('\\', '/')))
        results = self.evaluator.predict(dataset_encoded)
        self.is_suitable = collections.Counter(results)[0] / len(results) >= THRESHOLD_OF_BOOKING_PREDICTION
    
    
    def convert_list_to_data_frame_from_accommodate_infos(self):
		
        data_frame = {}

        for required_field in self.required_columns:
            data_frame[required_field] = []
        
        for val in self.survey_infos:
            amenities_list =  [amenity.lower().replace(' ', '_') for amenity in val['amenities']]
            for required_field in self.required_columns:
                if len(self.foreign_columns) > 0 and required_field in self.foreign_columns:
                    if required_field == 'property_type':
                        property_label = val[required_field]
                        if 'Private room' in property_label or 'Shared room' in property_label or 'Entire' in property_label :
                            data_frame[required_field].append('same_with_room_property')
                        else:
                            data_frame[required_field].append('other_property')
                    elif required_field == 'price':
                        if val['price'] < 99 :
                            data_frame[required_field].append('Cheap')
                        else:
                            data_frame[required_field].append('Expensive')
                elif required_field.startswith('have') or  required_field.startswith('give'):
                    data_frame[required_field].append(required_field in amenities_list)
                else:
                    data_frame[required_field].append(val[required_field])

        return data_frame


    def evaluate_survey_infos(self):
        
        data_frame = self.convert_list_to_data_frame_from_accommodate_infos()
        self.dataset = pd.DataFrame(data_frame)
        dataset_encoded = self.dataset.copy()
        for required_column in ['room_type', 'property_type', 'price']:
            labeler = load('{0}/static/surveys/models/accommodate/labeler_for_{1}.joblib'.format(
                                    os.getcwd().replace('\\', '/'), required_column))
            dataset_encoded[required_column] = labeler.transform(self.dataset[required_column])
        
        price_results = list(dataset_encoded['price'])
        dataset_encoded.drop(['price'], inplace=True, axis=1)
        self.normalizer = load('{}/static/surveys/models/accommodate/normalizer.joblib'.format(os.getcwd().replace('\\', '/')))
        dataset_encoded = self.normalizer.transform(dataset_encoded)
        self.evaluator = load('{}/static/surveys/models/accommodate/evaluator.joblib'.format(os.getcwd().replace('\\', '/')))
        results = self.evaluator.predict(dataset_encoded)
        
        values, frequencies = np.unique(np.logical_xor(results, price_results), return_counts=True)
        number_of_predict_true_price = frequencies[list(values).index(False)]
        
        self.price_list = list(self.dataset['price'])
        return number_of_predict_true_price / len(price_results)
        
    
    def evaluate_rated_host_infos(self):
        
        data_frame = self.convert_list_to_data_frame_from_accommodate_infos()
        self.dataset = pd.DataFrame(data_frame)
        dataset_encoded = self.dataset.copy()
        for required_column in ['room_type', 'property_type', 'price']:
            labeler = load('{0}/static/surveys/models/accommodate/labeler_for_{1}.joblib'.format(
                                    os.getcwd().replace('\\', '/'), required_column))
            dataset_encoded[required_column] = labeler.transform(self.dataset[required_column])
        
        price_results = list(dataset_encoded['price'])
        dataset_encoded.drop(['price'], inplace=True, axis=1)
        self.normalizer = load('{}/static/surveys/models/accommodate/normalizer.joblib'.format(os.getcwd().replace('\\', '/')))
        dataset_encoded = self.normalizer.transform(dataset_encoded)
        self.evaluator = load('{}/static/surveys/models/accommodate/evaluator.joblib'.format(os.getcwd().replace('\\', '/')))
        results = self.evaluator.predict(dataset_encoded)
        
        values, frequencies = np.unique(np.logical_xor(results, price_results), return_counts=True)
        number_of_predict_true_price = frequencies[list(values).index(False)]
        
        self.price_list.extend(list(self.dataset['price']))
        return number_of_predict_true_price / len(price_results)

    def get_appropriate_accommodate_places(self):
        """
			Find  accommodate demand is valid itself 
            and if is , get prices range recommended
   			by predicting price range with given values
  			"""
        
        self.foreign_columns = ['property_type', 'price']
        self.required_columns = [
                            'host_response_rate'
                            ,'host_acceptance_rate'       
                            ,'host_total_listings_count'  
                            ,'property_type'              
                            ,'room_type'
                            ,'price'
                            ,'bedrooms'                 
                            ,'minimum_nights'             
                            ,'maximum_nights'             
                            ,'have_parking'               
                            ,'have_workspace'             
                            ,'have_air_conditioning'      
                            ,'have_alarm'                 
                            ,'have_tv'                    
                            ,'have_washer'                
                            ,'have_stove'                 
                            ,'have_refrigerator'          
                            ,'give_special_hospitality'   
                            ,'have_heating']

        user = self.get_user()
        self.survey_infos =  [ survey_object.get_values_for_data_frame() for survey_object in AccommodateSurvey.objects.filter(user_id = user) ]
        if len(self.survey_infos) > 1 and len(self.survey_infos) % 2 == 0:
            self.survey_infos.pop()
        
        stability_rate_of_demand = self.evaluate_survey_infos()
        
        self.survey_infos =  []
        total_score_rate = 0.0

        for rated_object in HostRates().get_rated_hosts_by_user_id(user=user):
            total_score_rate = total_score_rate + rated_object['score']
            self.survey_infos.append(rated_object['host_info'])
            
        for rated_object in TipPlanRates().get_hosts_in_plans_by_user_id(user=user):
            total_score_rate = total_score_rate + rated_object['score']
            self.survey_infos.append(rated_object['host_info'])
        
        if total_score_rate != 0.0:
        
            number_of_survey_infos = len(self.survey_infos)
            if number_of_survey_infos > 1 and number_of_survey_infos % 2 == 0:
                self.survey_infos.pop()
                number_of_survey_infos = number_of_survey_infos - 1
            
            stability_rate_of_demand = (stability_rate_of_demand + (self.evaluate_rated_host_infos() * (total_score_rate / (number_of_survey_infos * 5)))) / 2
        
        if stability_rate_of_demand >= THRESHOLD_OF_ACCOMMODATE_PREDICTION:
            price_range = max(set(self.price_list), key = self.price_list.count)
            self.recommended_host_infos = { 'result': True, 'price_range': '99-400' if price_range == 'Expensive' else '8-98'}

    def get_places_from_rated_plans(self):
        
        trip_places_in_plans = TipPlanRates().get_trip_places_in_plans_by_user_id(user=self.get_user())
        
        result_plans = []
        for trip_places_in_plan in trip_places_in_plans :
            place_type_list = []
            score = trip_places_in_plan['score']
            for place_info in trip_places_in_plan['place_list'] :
                place_type_list.extend([ place_type for place_type in place_info['place_types']])
            place_type_dist = collections.Counter(place_type_list)
            
            total_frequency = len(place_type_list)
            result_plans.append({
                "rate_of_religious_place" : (place_type_dist[self.place_types[1]] + place_type_dist[self.place_types[2]] + place_type_dist[self.place_types[3]]) * (score / total_frequency),
                "rate_of_parks" : (place_type_dist[self.place_types[3]] + place_type_dist[self.place_types[4]]) * (score / total_frequency),
                "rate_of_theaters" : place_type_dist[self.place_types[5]]* (score / total_frequency),
                "rate_of_mall" : place_type_dist[self.place_types[6]]* (score / total_frequency),
                "rate_of_museum" : place_type_dist[self.place_types[7]]* (score / total_frequency),
                "rate_of_art_gallery" : place_type_dist[self.place_types[8]]* (score / total_frequency),
                "rate_of_zoo" : place_type_dist[self.place_types[13]]* (score / total_frequency),
                "rate_of_restaurant" : place_type_dist[self.place_types[9]]* (score / total_frequency),
                "rate_of_pubs" : (place_type_dist[self.place_types[10]] + place_type_dist[self.place_types[12]]) * (score / total_frequency),
                "rate_of_gym" : place_type_dist[self.place_types[11]]* (score / total_frequency),
                "rate_of_spa" : (place_type_dist[self.place_types[14]] + place_type_dist[self.place_types[15]]) * (score / total_frequency),
                "rate_of_cafe" : place_type_dist[self.place_types[16]]* (score / total_frequency),
                "rate_of_viewpoints" : place_type_dist[self.place_types[17]]* (score / total_frequency),
                "rate_of_monument" : place_type_dist[self.place_types[17]]* (score / total_frequency)
                })
        
        self.survey_infos.extend(result_plans)
    
    
    
    def convert_list_to_data_frame_trip_survey_infos(self):
		
        data_frame = {}

        for required_field in self.required_properties:
            data_frame[required_field] = []
        
        number_of_properties = len(self.required_properties)
        for val in self.survey_infos:
            for i in range(number_of_properties):
                data_frame[self.required_properties[i]].append(val[self.required_columns[i]])

        return data_frame


    def get_cluster_of_trip_place_around_by_user(self):
        """
            get cluster of trip place near to accommodate place
            for given user
            """
        self.required_columns = [
                            'rate_of_religious_place'       
                            ,'rate_of_parks'          
                            ,'rate_of_theaters'       
                            ,'rate_of_mall'        
                            ,'rate_of_museum'          
                            ,'rate_of_art_gallery'            
                            ,'rate_of_zoo'           
                            ,'rate_of_restaurant'    
                            ,'rate_of_pubs'      
                            ,'rate_of_gym'   
                            ,'rate_of_spa'  
                            ,'rate_of_cafe'          
                            ,'rate_of_viewpoints'    
                            ,'rate_of_monument'
        ]

        self.required_properties = [
                            'churches'       
                            ,'parks'          
                            ,'theatres'       
                            ,'museums'        
                            ,'malls'          
                            ,'zoo'            
                            ,'gyms'           
                            ,'restaurants'    
                            ,'pubs/bars'      
                            ,'art galleries'   
                            ,'beauty & spas'  
                            ,'cafes'          
                            ,'view points'    
                            ,'monuments']

        user = self.get_user()
        self.survey_infos =  list(TripSurvey.objects.filter(user_id = user).values())
        self.get_places_from_rated_plans()
        if len(self.survey_infos) > 1 and len(self.survey_infos) % 2 == 0:
            self.survey_infos.pop()
        data_frame = self.convert_list_to_data_frame_trip_survey_infos()
        self.dataset = pd.DataFrame(data_frame)
        dataset_scaled = self.dataset.copy()

        self.normalizer = load('{}/static/surveys/models/trip_place/scaler.joblib'.format(os.getcwd().replace('\\', '/')))
        dataset_scaled = self.normalizer.transform(dataset_scaled)
        self.normalizer2 = load('{}/static/surveys/models/trip_place/pca.joblib'.format(os.getcwd().replace('\\', '/')))
        dataset__pac_scaled = self.normalizer2.transform(dataset_scaled)
        self.evaluator = load('{}/static/surveys/models/trip_place/clusterer.joblib'.format(os.getcwd().replace('\\', '/')))
        self.user_clusters = self.evaluator.predict(dataset__pac_scaled)


    def get_cluster_of_host_by_place_types(self, host_id):
        
        """
            Get cluster of host by ite nearest
            trip place types
            """
        self.nearest_trip_places = TripPlaces().get_nearest_trip_places_around_the_host(host_id)
            
        if len(self.nearest_trip_places) > 0:

            number_of_places_by_type = np.zeros(len(self.place_types))
            rating_by_type = np.zeros(len(self.place_types)) 
            for nearest_trip_place in self.nearest_trip_places:
                rating_and_types = TripPlaces().get_rating_and_types(place_id = nearest_trip_place[6])
                for the_type in rating_and_types['types']:
                    index = self.place_types.index(the_type)
                    rating_by_type[index] = rating_by_type[index] + rating_and_types['rating']
                    number_of_places_by_type[index] = number_of_places_by_type[index] + 1
                    
            last_ratings = np.nan_to_num(rating_by_type / number_of_places_by_type)

            dataset = pd.DataFrame({ 'churches': [(last_ratings[0] + last_ratings[1] + last_ratings[2]) / 3],
                                    'parks': [(last_ratings[3] + last_ratings[4]) / 2], 
                                    'theatres': [last_ratings[5]], 
                                    'museums': [ last_ratings[6] ],
                                    'malls': [ last_ratings[7] ],
                                    'zoo': [ last_ratings[8] ],
                                    'gyms': [last_ratings[13]], 
                                    'restaurants': [ last_ratings[9] ], 
                                    'pubs/bars': [(last_ratings[10] + last_ratings[12]) / 2],
                                    'art galleries': [ last_ratings[11] ], 
                                    'beauty & spas': [ (last_ratings[14] + last_ratings[15]) / 2 ], 
                                    'cafes': [ last_ratings[16] ], 
                                    'view points': [ last_ratings[17] ], 
                                    'monuments': [last_ratings[17]] 
                                    })
            dataset_scaled = dataset.copy()

            self.normalizer = load('{}/static/surveys/models/trip_place/scaler.joblib'.format(os.getcwd().replace('\\', '/')))
            dataset_scaled = self.normalizer.transform(dataset_scaled)
            self.normalizer2 = load('{}/static/surveys/models/trip_place/pca.joblib'.format(os.getcwd().replace('\\', '/')))
            dataset__pac_scaled = self.normalizer2.transform(dataset_scaled)
            self.evaluator = load('{}/static/surveys/models/trip_place/clusterer.joblib'.format(os.getcwd().replace('\\', '/')))
            self.host_cluster = self.evaluator.predict(dataset__pac_scaled)[0]


