
import random
from django.db.models import (Model, 
								AutoField, 
        						IntegerField, 
								CharField, 
								DateField, 
								FloatField, 
								BooleanField, 
								ForeignKey,
								Q,
        						Count,
              					Avg,
								CASCADE)
from utils.models import Property, Amenities
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


class Host(Model):

	id = AutoField(primary_key=True, db_index=False)
	listing_id = IntegerField(null=True)
	host_id = IntegerField(null=True)
	name = CharField(max_length=800, null=True)
	host_since = DateField(null=True)
	host_location = CharField(max_length=800, null=True)
	host_response_time = CharField(max_length=30,null=True)
	host_response_rate = FloatField(null=True)
	host_acceptance_rate = FloatField(null=True)
	host_total_listings_count = FloatField(null=True)
	host_identity_verified = BooleanField(null=True)
	city = CharField(max_length=20, null=True)
	district = CharField(max_length=20, null=True)
	neighborhood = CharField(max_length=30, null=True)
	longitude = FloatField()
	latitude = FloatField()
	room_type = CharField(max_length=20, null=True)
	property_type = ForeignKey(Property, on_delete=CASCADE,related_name='+', null=True)
	accommodates = IntegerField(null=True)
	price = FloatField(null=True)
	bedrooms = IntegerField()
	amenities = CharField(max_length=1544,null=True)
	minimum_nights = IntegerField(null=True)
	maximum_nights = IntegerField(null=True)
	review_scores_rating = IntegerField(null=True)
	review_scores_accuracy = IntegerField(null=True)
	review_scores_cleanliness = IntegerField(null=True)
	review_scores_checkin = IntegerField(null=True)
	review_scores_communication = IntegerField(null=True)
	review_scores_location = IntegerField(null=True)
	review_scores_value = IntegerField(null=True)
	instant_bookable = BooleanField(null=True)
		
	def get_as_list_randomly(self, number = 9):
		hosts = list(Host.objects.all()[300:400])
		hosts = random.sample(hosts, number)
		return hosts

	def get_property_type_description(self, id):
		return Property.objects.filter(id = id).get().label

	def give_random_result(self, hosts, number = 9):
     	
		hosts = random.sample(hosts, number)
		for host in hosts:
			property_description = self.get_property_type_description(host['property_type'])
			del host['property_type']
			host['property'] = property_description
		return hosts

	def get_name_price_property_type_randomly(self, number = 9):
		hosts = list(Host.objects.all()
               		.values('id', 'name', 'property_type', 'price', 'review_scores_rating')[0:400])

		return self.give_random_result(hosts, number)

	def get_name_price_property_type_randomly_in_price_range(self, min_price, max_price, number = 9):
		hosts = list(Host.objects.filter(price__lt=max_price, price__gt=min_price)
               		.values('id', 'name', 'property_type', 'price', 'review_scores_rating')[100:200])

		return self.give_random_result(hosts, number)

	def get_data_frame_datas(self):
		host_object = Host.objects.get(id=self.id)
		return ''

	def get_host_by_id_range(self,start_offset, length):
		return list(Host.objects.all().values('id', 'name', 'review_scores_rating')
              							.order_by("id")[start_offset: start_offset + length])
  
	def get_coordinates_by_id_range(self,start_offset, length):
		return list(Host.objects.all().values('id', 'longitude', 'latitude')
              							.order_by("id")[start_offset: start_offset + length])
  
	def search_hosts_by_name(self, keyword, start_offset, length):
		return list(Host.objects.filter(Q(name__icontains=keyword)).values('id', 'name', 'review_scores_rating')
              							.order_by("id")[start_offset: start_offset + length])

	def get_host_url(self):
		return f"/host_info/get-detail/{self.id}"

	def get_host_by_id(self):
		host = model_to_dict(Host.objects.get(id = self.id))
		property_description = self.get_property_type_description(host['property_type'])
		the_host = {}
		the_host['id'] = host['id']
		the_host['name'] = host['name']
		the_host['property'] = property_description
		the_host['price'] = host['price']
		the_host['review_scores_rating'] = host['review_scores_rating']
		return the_host

	def get_amenities_in_array(self):
		return self.amenities.replace("]", "").replace("[", "").replace("\'", " ")

	def set_amenities_and_others_for_evaluator(self):
		amenities_list = self.get_amenities_in_array().lower()
		amenities = []

		if 'parking' in amenities_list:
			amenities.append('Have Parking')
		if 'workspace' in amenities_list:
			amenities.append('Have Parking')
		if 'air conditioning' in amenities_list:
			amenities.append('Air Conditioning')
		if 'alarm' in amenities_list:
			amenities.append('Have Alarm')
		if 'tv' in amenities_list:
			amenities.append('Have Tv')
		if 'washer' in amenities_list:
			amenities.append('Have Washer')
		if 'stove' in amenities_list:
			amenities.append('Have Stove')
		if 'refrigerator' in amenities_list:
			amenities.append('Have Refrigerator')
		if 'host greets you' in amenities_list:
			amenities.append('Give Special Hospitality')
		if 'heating' in amenities_list:
			amenities.append('Have Heating')
   
		host_info = {
			'host_response_rate': self.host_response_rate,
			'host_acceptance_rate' : self.host_acceptance_rate,
			'host_total_listings_count' : self.host_total_listings_count,
			'property_type' : self.property_type.label,
			'room_type': self.room_type,
			'price': self.price,
			'bedrooms' : self.bedrooms,
			'minimum_nights' : self.minimum_nights,
			'maximum_nights' : self.maximum_nights,
   			"amenities": amenities
		}
  
		return host_info



class HostRates(Model):
    
	id = AutoField(primary_key=True, db_index=False)
	user = ForeignKey(User, on_delete=CASCADE,related_name='+')
	host = ForeignKey(Host, on_delete=CASCADE,related_name='+')
	rate_score = FloatField()
    
	def get_rate(self, user_id, host_id):

		user = User.objects.get(id = user_id)
		host = Host.objects.get(id = host_id)

		host_rate = HostRates.objects.filter(Q(user = user) & Q(host = host)).last()
		return host_rate.rate_score if host_rate != None else None;

	def get_all_rates(self, user_id):
     
		user = User.objects.get(id = user_id)
		all_rated_hosts = [record['host'] for record in list(HostRates.objects.filter(user = user).values('host').annotate(idcount=Count('id')).order_by())]
		
		all_host_rates = []
		for rated_host in all_rated_hosts:
			host = Host.objects.get(id = rated_host)
			rate_values =  HostRates.objects.filter(Q(user = user) & Q(host = host)).last()		
			all_host_rates.append({
					'id' : host.id,
					'name' : host.name,
					'rate_score': rate_values.rate_score
			})
		
		return all_host_rates


	def get_rated_hosts_by_user_id(self, user):
		
		all_rated_hosts = [Host.objects.get(id = record['host']) for record in list(HostRates.objects.filter(user = user).values('host').annotate(idcount=Count('id')).order_by())]
	
		result_plans = []
		for rated_host in all_rated_hosts:
			host = rated_host # Host.objects.get(id = rated_host)
			host_info = host.set_amenities_and_others_for_evaluator()
			score = HostRates.objects.filter(Q(user = user) & Q(host = host)).aggregate(Avg('rate_score'))['rate_score__avg']
			
			result_plans.append({ "score" : score, "host_info": host_info})

		return result_plans

    
	def give_rate(self,user_id, host_id):
		
		user = User.objects.get(id = user_id)
		host = Host.objects.get(id = host_id)
        
		new_rate = HostRates.objects.create(
								user = user,
								host = host,
								rate_score = self.rate_score)
        
		print(f" New rate crated in id : {new_rate.id} ")
        