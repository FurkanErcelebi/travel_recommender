
from django.forms.models import model_to_dict
from django.db.models import Model, AutoField, DateField, ForeignKey, FloatField, CASCADE, Q, Count, Avg
from django.contrib.auth.models import User
from host_info.models import Host
from travel_search.models import TripPlaces


class TripPlan(Model):
	
	id = AutoField(unique=True, primary_key=True, auto_created=True, db_index=False)
	start_date = DateField()
	end_date = DateField()
	user_id = ForeignKey(User, on_delete=CASCADE,related_name='+')
	host_id  = ForeignKey(Host, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place1_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place2_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place3_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place4_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place5_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place6_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place7_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place8_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place9_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_place10_id = ForeignKey(TripPlaces, on_delete=CASCADE,related_name='+', default=None, blank=True, null=True)
 
	def is_plan_exist_in_specific_range(self):
		return list(TripPlan.objects.filter(Q(end_date__gt = self.start_date) | Q(start_date__lt = self.end_date) ))

	def create_trip_plan(self, user_id, host_id, place_id_array):
		
		current_user = User.objects.get(id = user_id)
		the_host = Host.objects.get(id = host_id)
		tripPlan = TripPlan.objects.create(user_id = current_user,
											host_id = the_host,
      									start_date = self.start_date,
										end_date = self.end_date)
		i = 1
		for place_id in place_id_array:
			match i:
				case 1:
					tripPlan.trip_place1_id = TripPlaces.objects.get(id = place_id)
				case 2:
					tripPlan.trip_place2_id = TripPlaces.objects.get(id = place_id)
				case 3:
					tripPlan.trip_place3_id = TripPlaces.objects.get(id = place_id)
				case 4:
					tripPlan.trip_place4_id = TripPlaces.objects.get(id = place_id)
				case 5:
					tripPlan.trip_place5_id = TripPlaces.objects.get(id = place_id)
				case 6:
					tripPlan.trip_place6_id = TripPlaces.objects.get(id = place_id)
				case 7:
					tripPlan.trip_place7_id = TripPlaces.objects.get(id = place_id)
				case 8:
					tripPlan.trip_place8_id = TripPlaces.objects.get(id = place_id)
				case 9:
					tripPlan.trip_place9_id = TripPlaces.objects.get(id = place_id)
				case 10:
					tripPlan.trip_place10_id = TripPlaces.objects.get(id = place_id)
			
     
			i = i + 1
     
		tripPlan.save()
  
  
	# def plan_exist_between_specified_dates():
	# 	TripPlan.objects.filter(start_date__range=)
	# 	pass
		
  
	def get_trip_plan_by_user_id(self, user_id):
		trip_plans = list(TripPlan.objects.filter(user_id = user_id).values())
		for trip_plan in trip_plans:
			del trip_plan['user_id_id']
			host_info = Host(id = trip_plan['host_id_id']).get_host_by_id()
			del trip_plan['host_id_id']
			trip_plan['host_infos'] = host_info
			rateValue = TipPlanRates().get_rate(user_id, trip_plan['id'])
			trip_plan['trip_rate'] = rateValue
			trip_place_list = []
			for i in range(10):
				trip_place_column = 'trip_place{0}_id_id'.format(i + 1)
				place_id = trip_plan[trip_place_column]
				if place_id != None:
					trip_place =  TripPlaces(id = place_id).get_trip_place_by_id()
					del trip_plan[trip_place_column]
					trip_place_list.append(trip_place)

			trip_plan['trip_places'] = trip_place_list

   
		return trip_plans

	def delete_trip_plan(self, id):
		TripPlan.objects.filter(id = id).delete()


class TipPlanRates(Model):
    
	id = AutoField(primary_key=True, db_index=False)
	user = ForeignKey(User, on_delete=CASCADE,related_name='+')
	plan = ForeignKey(TripPlan, on_delete=CASCADE,related_name='+')
	rate_score = FloatField()
    
	def get_rate(self, user_id, plan_id):

		user = User.objects.get(id = user_id)
		tripPlan = TripPlan.objects.get(id = plan_id)

		trip_plan_rate = TipPlanRates.objects.filter(Q(user = user) & Q(plan = tripPlan)).last()
		return trip_plan_rate.rate_score if trip_plan_rate != None else None
    	
     
	def get_hosts_in_plans_by_user_id(self, user):
		
		result_plans = []
		for the_plan in list(TipPlanRates.objects.filter(user = user).values('plan', 'rate_score')):
			plan_object = model_to_dict(TripPlan.objects.get(id = the_plan['plan']))
			host_info = Host.objects.get(id=plan_object['host_id']).set_amenities_and_others_for_evaluator()
			
			result_plans.append({ "score" : the_plan['rate_score'], "host_info": host_info})

		return result_plans
	

	def get_trip_places_in_plans_by_user_id(self, user):
		
		result_plans = []

		all_rated_plans = [TripPlan.objects.get(id = record['plan']) for record in list(TipPlanRates.objects.filter(user = user).values('plan').annotate(idcount=Count('id')).order_by())]
  
		for rated_plan in all_rated_plans:
			plan_object = model_to_dict(rated_plan)
			score = TipPlanRates.objects.filter(Q(user=user) & Q(plan=rated_plan)).aggregate(Avg('rate_score'))['rate_score__avg']
			plan_item = { "score" : score, "place_list": []}
			for i in range(1, 11):
				place_column = 'trip_place{}_id'.format(i)
				if plan_object[place_column] != None:
					place_info = { }
					place_info['place_types'] = TripPlaces.objects.get(id=plan_object[place_column]).get_types_in_array()
					plan_item['place_list'].append(place_info)

			result_plans.append(plan_item)

		return result_plans
    

	def get_all_rates(self, user_id):
     
		user = User.objects.get(id = user_id)
  
		all_rated_plans = [record['plan'] for record in list(TipPlanRates.objects.filter(user = user).values('plan').annotate(idcount=Count('id')).order_by())]
		
		all_plan_rates = []
		for rated_plan in all_rated_plans:
			plan = TripPlan.objects.get(id = rated_plan)
			rate_values =  TipPlanRates.objects.filter(Q(user = user) & Q(plan = plan)).last()		
			all_plan_rates.append({
					'id' : plan.id,
					'name' : 'Travel to {}'.format(plan.host_id.name),
					'rate_score': rate_values.rate_score
			})
		
		return all_plan_rates
		# all_trip_plan_rates = list(TipPlanRates.objects.filter(user = user)
        #                      					.values('id', 'plan', 'rate_score'))
		# for all_trip_plan_rate in all_trip_plan_rates:
		# 	all_trip_plan_rate['name'] = all_trip_plan_rate['plan']
		# 	del all_trip_plan_rate['plan']
   
		# return all_trip_plan_rates
    
    
	def give_rate(self,user_id, plan_id):
		
		user = User.objects.get(id = user_id)
		plan = TripPlan.objects.get(id = plan_id)
        
		new_rate = TipPlanRates.objects.create(
								user = user,
								plan = plan,
								rate_score = self.rate_score)
        
		print(f" New rate crated in id : {new_rate.id} ")
	
  
