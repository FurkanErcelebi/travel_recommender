from django import forms  
from django.forms.widgets import Input

from utils.models import *
from personal_info.models import PersonalInfo
from .models import *
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


WIDTH20 = 'width: 20%;'
TRIPRANGEWIDGET_W_STEP = Input(attrs={ 'type':'range', 'class':'form-range', 'step': "0.01", 'min':'0', 'max':'1'})
NUNBERINPUTWIDGET = forms.TextInput(attrs={'type':'number','class':'form-control'})



def set_number_input(min = 0, max = 0):
    attrs = {'type':'number','class':'form-control survey-response'}
    #attrs['style'] = WIDTH20
    if min > -1:
        attrs['min'] = str(min)
    
    if max > 0:
        attrs['max'] = str(max)
    
    return forms.TextInput(attrs=attrs)

def set_radio_input(choices):
    
    return forms.RadioSelect(choices=choices,attrs={'class': 'form-check-input'})


class BaseSurveyForm(forms.Form):
    def show_infos(self, user_id):
        pass
    def save_survey(self, user_id):
        pass
    def update_survey(self, user_id):
        pass

class PersonalSurveyForm(BaseSurveyForm):
 	# change label
	lead_time = forms.CharField(label='How many days can you arrive at the place where you booking ?', 
								help_text=mark_safe("<p>You must give value between 0 and 74 </p>"),
								widget=set_number_input(1, 74))
 
	stays_in_weekend_nights = forms.CharField(label='How many days would you spend at accommodate in weekend nights ?', 
											help_text=mark_safe("<p>You must give value between 1 and 2 </p>"),
											widget=set_number_input(0,2))
 
	stays_in_week_nights = forms.CharField(label='How many days would you spend at accommodate in week nights ?',
											help_text=mark_safe("<p>You must give value between 1 and 6 </p>"),
											widget=set_number_input(1, 6))
 
	adults = forms.CharField(label='How many adults would you go like to go to accommodate place?',
											help_text=mark_safe("<p>You must give value between 0 and 55 </p>"),
											widget=set_number_input(0,55))
 
	babies = forms.CharField(label='How many babies would you go like to go to accommodate place?',
											help_text=mark_safe("<p>You must give value between 0 and 10 </p>"),
											widget=set_number_input(0,10))
 
	children = forms.CharField(label='How many children would you go like to go to accommodate place?',
											help_text=mark_safe("<p>You must give value between 0 and 10 </p>"),
											widget=set_number_input(0,10))
 
	booking_changes = forms.CharField(label='How many times would you change or do amendment in bookings ?', 
								help_text=mark_safe("<p>You must give value between 0 and 21 </p>"),
								widget=set_number_input(0, 21))
 
	days_in_waiting_list = forms.CharField(label=" ".join(["Have you patient for  waiting to booking is confirmed.",
                                        				"If so how many days would you wait until confirmed ? "]), 
											help_text=mark_safe("<p>You must give value between 0 and 40 </p>"),
											widget=set_number_input(0,40))
 
	adr = forms.CharField(label='How many lodging transaction would you do i daily basis ?',
											help_text=mark_safe("<p>You must give value between 0 and 5400 </p>"),
											widget=set_number_input(0,5400))
 
	required_car_parking_spaces = forms.CharField(label='Would you need to parking space for your cars , if so how many parking space?',
											help_text=mark_safe("<p>You must give value between 0 and 8 </p>"),
											widget=set_number_input(0,8))
 
	total_of_special_requests = forms.CharField(label='How many special request would yo do in booking process ?',
											help_text=mark_safe("<p>You must give value between 0 and 5 </p>"),
											widget=set_number_input(0,5))
 
	hotel = forms.CharField(label='Which room range would you prefer for acommodating place ?', 
								help_text=mark_safe("<p>You must select one of them </p>"),
								widget=set_radio_input(HOTELTYPES))
 
	is_repeated_guest = forms.CharField(label='Would you booking for same place in multiple times ?',
									widget=set_radio_input([('1', 'No'),('2', 'Yes')]))
 
 
	meal = forms.CharField(label='What type of meal service would you prefer in accommodation place ?',
											help_text=mark_safe("""<p>Undefined/SC – no meal package</p>
																	<p> BB – Bed & Breakfast;</p>
																	<p> HB – Half board(breakfast and one other 
                 																meal , usually dinner)</p>
																	<p> FB – Full board(breakfast,lunch and dinner)</p>"""),
											widget=set_radio_input(MEALTYPES))
 
	market_segment = forms.CharField(label='In case of selecting market segment booking process , what type of segment would you select?',
											help_text=mark_safe(""" <p>TA - TravelAgents </p>
                               										<p>TO - Tour Operators </p>"""),
											widget=set_radio_input(MARKET))
 
	distribution_channel = forms.CharField(label='What distribution type would you prefer in providence of traveling to accommodate place?',
											help_text=mark_safe(""" <p>TA - TravelAgents </p>
                               										<p>TO - Tour Operators </p> """),
											widget=set_radio_input(DISTRIBUTION))
 
	deposit_type = forms.CharField(label='Would you do make deposit for guarantee the booking , if so , Which type?',
											help_text=mark_safe("""<p>No Deposit – no deposit was made</p>
                               										<p>Non Refund – a deposit was made in
                                         								the value of the total stay cost;</p>
                               										<p>Refundable – a deposit was made with
																		a value under the total cost of stay.</p>"""),
											widget=set_radio_input(DEPOSITTYPE))
 
	customer_type = forms.CharField(label='What type of booking process would you do?',
											help_text=mark_safe(""" <p> Contract – when the booking has an 
                               										allotment or other type of contract associated to it;</p>
																	<p> Group – when the booking is associated to a group;</p>
																	<p> Transient – when thebookingisnot part ofagrouporcontract,
                 														andisnot associated toothertransientbooking;</p>
																	<p> Transient-party – when thebookingis transient, 
                 														butisassociatedtoatleast other transientbooking</p>"""),
											widget=set_radio_input(CUSTOMERTYPE))



	def show_infos(self, user_id):
     

		user = User.objects.get(id = user_id)
		hotel = Hotels.objects.get(type = self.cleaned_data['hotel'])
		meal = Meals.objects.get(type = self.cleaned_data['meal'])
		market_segment = Market.objects.get(type = self.cleaned_data['market_segment'])
		distribution_channel = Distribution.objects.get(type = self.cleaned_data['distribution_channel'])
		deposit_type = Deposit.objects.get(type = self.cleaned_data['deposit_type'])
		customer_type = Customer.objects.get(type = self.cleaned_data['customer_type'])
  
		lead_time = self.cleaned_data['lead_time']
		stays_in_weekend_nights = self.cleaned_data['stays_in_weekend_nights']
		stays_in_week_nights = self.cleaned_data['stays_in_week_nights']
		adults = self.cleaned_data['adults']
		babies = self.cleaned_data['babies']
		children = self.cleaned_data['children']
		booking_changes = self.cleaned_data['booking_changes']
		days_in_waiting_list = self.cleaned_data['days_in_waiting_list']
		adr = self.cleaned_data['adr']
		required_car_parking_spaces = self.cleaned_data['required_car_parking_spaces']
		total_of_special_requests = self.cleaned_data['total_of_special_requests']
		is_repeated_guest = self.cleaned_data['is_repeated_guest']

		print("""New Personal Survey for user {} Responses: {}, {}, {}
        										, {}, {}, {}, {}
                  								, {}, {}, {}
                  								, {}, {}, {}
                  								, {}, {}, {}
                  								, {}, {}, """.format(user, lead_time,
														stays_in_weekend_nights,
														stays_in_week_nights,
														adults,
														babies,
              											children,
														booking_changes,
														days_in_waiting_list,
														adr,
														required_car_parking_spaces,
														total_of_special_requests,
														is_repeated_guest,
														hotel,
														meal,
														market_segment,
														distribution_channel,
														deposit_type,
														customer_type
              ))
	
	def save_survey(self, user_id):
     
		is_repeated_guest = int(self.cleaned_data['is_repeated_guest']) - 1
		
		new_personal_survey = PersonalSurvey(
								lead_time = self.cleaned_data['lead_time'],
								stays_in_weekend_nights = self.cleaned_data['stays_in_weekend_nights'],
								stays_in_week_nights = self.cleaned_data['stays_in_week_nights'],
								adults = self.cleaned_data['adults'],
								babies = self.cleaned_data['babies'],
								children = self.cleaned_data['children'],
								booking_changes = self.cleaned_data['booking_changes'],
								days_in_waiting_list = self.cleaned_data['days_in_waiting_list'],
								adr = self.cleaned_data['adr'],
								required_car_parking_spaces = self.cleaned_data['required_car_parking_spaces'],
								total_of_special_requests = self.cleaned_data['total_of_special_requests'],
								is_repeated_guest = is_repeated_guest
							).insert_new_instance(user_id, 
													self.cleaned_data['hotel'],
													self.cleaned_data['meal'],
													self.cleaned_data['market_segment'],
													self.cleaned_data['distribution_channel'],
													self.cleaned_data['deposit_type'],
													self.cleaned_data['customer_type'])
       
		PersonalInfo().set_personal_survey_in_info(user_id, new_personal_survey)
       
	
		print("New personal Survey created")
  
	def get_all_values(self):
		print(f"customer type : {self.customer_type}")


class AccommodateSurveyForm(BaseSurveyForm):
    
    host_total_listings_count = forms.CharField(label='how many maximum nights would you spend in acommodate?',
									help_text=mark_safe("<p>You must give value between 0 and 7235 </p>"),
									widget=set_number_input(0,7235))
    
    minimum_nights = forms.CharField(label='how many maximum nights would you spend in acommodate?',
									help_text=mark_safe("<p>You must give value between 1 and 1124 </p>"),
									widget=set_number_input(0,1124))
    
    maximum_nights = forms.CharField(label='how many minimum nights would you spend in acommodate?',
									help_text=mark_safe("<p>You must give value between 0 and 20000000 </p>"),
									widget=set_number_input(0,20000000))
    
    bedrooms = forms.CharField(label='how many bedroom nights would you prefer in acommodate ?', 
									help_text=mark_safe("<p>You must give value between 1 and 21 </p>"),
									widget=set_number_input(1,21))
    
    price = forms.CharField(label='What privce range do you prefer for price of hosting accommodate?',
									help_text=mark_safe("<p>You must give value between 8 and 399 </p>"),
									widget=set_number_input(8,399))
    
    host_response_rate = forms.CharField(label="What frequent would you want to get response for booking send to the host ?"
                                        , widget= TRIPRANGEWIDGET_W_STEP)
    
    host_acceptance_rate = forms.CharField(label="What percentage of acceptance would you want from host to accept booking requests ?"
                                        ,widget= TRIPRANGEWIDGET_W_STEP)
    
    property_type = forms.ChoiceField(label='What type of property type would you prefer in accommodate ?',
									choices=PROPERTYTYPES,widget=forms.Select(attrs={
							        	'class': 'form-select',
							        	'aria-label': 'Default select example'
							        	}))
 
    room_type = forms.ChoiceField(label='What type of room type would you prefer in accommodate ?',
									choices=ROOMTYPES,widget=forms.Select(attrs={
							        	'class': 'form-select',
							        	'aria-label': 'Default select example'
							        	}))
 
    amenities = forms.MultipleChoiceField(label='Which one or ones of amenities would you prefer that accommodates provide ?',
									choices=AMENITIES, widget=forms.CheckboxSelectMultiple(
                    					attrs={
							        	'class': 'form-check-input',
							        	'aria-label': 'Default select example'
							        	}))
 
    def show_infos(self, user_id):
        
        user = User.objects.get(id = user_id)
        property_type = Property.objects.get(type = self.cleaned_data['property_type'])
        room_type = Rooms.objects.get(type = self.cleaned_data['room_type'])
        amenities_list = []
        selected_amenities = self.cleaned_data['amenities']
        for selected_amenity in selected_amenities:
            amenities_list.append(Amenities.objects.get(type = selected_amenity))
    
        host_total_listings_count = self.cleaned_data['host_total_listings_count']
        minimum_nights = self.cleaned_data['minimum_nights']
        maximum_nights = self.cleaned_data['maximum_nights']
        bedrooms = self.cleaned_data['bedrooms']
        price = self.cleaned_data['price']
        host_response_rate = self.cleaned_data['host_response_rate']
        host_acceptance_rate = self.cleaned_data['host_acceptance_rate']

        print("""New accommodate survey responses for user {} : {}, {}, {}, 
              										{}, {}, {},
                        							{}, {}, {}, {}""".format(user, host_total_listings_count,
																				minimum_nights,
																				maximum_nights,
																				bedrooms,
																				price,
																				host_response_rate,
																				host_acceptance_rate,
																				property_type,
																				room_type,
																				amenities_list))
  
    def save_survey(self, user_id):
    
        new_accommodate_survey = AccommodateSurvey(
            	host_total_listings_count = self.cleaned_data['host_total_listings_count'],
				minimum_nights = self.cleaned_data['minimum_nights'],
				maximum_nights = self.cleaned_data['maximum_nights'],
				bedrooms = self.cleaned_data['bedrooms'],
				price = self.cleaned_data['price'],
				host_response_rate = self.cleaned_data['host_response_rate'],
				host_acceptance_rate = self.cleaned_data['host_acceptance_rate']
    	).insert_new_instance(user_id ,
                            	self.cleaned_data['property_type'],
								self.cleaned_data['room_type'],
        						self.cleaned_data['amenities'])
     
        PersonalInfo().set_accommodate_survey_in_info(user_id, new_accommodate_survey)
        
        print("New accommodate survey created")


#What level of preference is {trip place} for you ?"
class TripSurveyForm(BaseSurveyForm):
    
    religious_place_preference_rate = forms.CharField(label="Religious Place", widget= TRIPRANGEWIDGET_W_STEP)
    parks_preference_rate = forms.CharField(label="Parks", widget= TRIPRANGEWIDGET_W_STEP)
    theaters_preference_rate = forms.CharField(label="Movie Theaters", widget= TRIPRANGEWIDGET_W_STEP)
    mall_preference_rate = forms.CharField(label="Mall", widget= TRIPRANGEWIDGET_W_STEP)
    museum_preference_rate = forms.CharField(label="Museum", widget= TRIPRANGEWIDGET_W_STEP)
    zoo_preference_rate = forms.CharField(label="Zoo", widget= TRIPRANGEWIDGET_W_STEP)
    restaurant_preference_rate =  forms.CharField(label="Restaurant", widget= TRIPRANGEWIDGET_W_STEP)
    pubs_preference_rate = forms.CharField(label="Pubs / Bars", widget= TRIPRANGEWIDGET_W_STEP)
    art_gallery_preference_rate = forms.CharField(label="Art Gallery", widget= TRIPRANGEWIDGET_W_STEP)
    gym_preference_rate = forms.CharField(label="Gym", widget= TRIPRANGEWIDGET_W_STEP)
    beauty_spa_preference_rate = forms.CharField(label="Beauty Spa", widget= TRIPRANGEWIDGET_W_STEP)
    cafe_preference_rate = forms.CharField(label="Cafe", widget= TRIPRANGEWIDGET_W_STEP)
    viewpoints_preference_rate = forms.CharField(label="Viewpoints", widget= TRIPRANGEWIDGET_W_STEP)
    monument_preference_rate = forms.CharField(label="Monuments", widget= TRIPRANGEWIDGET_W_STEP)
    
    def show_infos(self, user_id):
        
        user = User.objects.get(id = user_id)
        religious_place_preference_rate = self.cleaned_data['beach_preference_rate']
        parks_preference_rate = self.cleaned_data['parks_preference_rate']
        theaters_preference_rate = self.cleaned_data['theaters_preference_rate']
        mall_preference_rate = self.cleaned_data['mall_preference_rate']
        museum_preference_rate = self.cleaned_data['museum_preference_rate']
        art_gallery_preference_rate = self.cleaned_data['art_gallery_preference_rate']
        zoo_preference_rate = self.cleaned_data['zoo_preference_rate']
        restaurant_preference_rate = self.cleaned_data['restaurant_preference_rate']
        pubs_preference_rate = self.cleaned_data['pubs_preference_rate']
        gym_preference_rate = self.cleaned_data['gym_preference_rate']
        spa_preference_rate = self.cleaned_data['spa_preference_rate']
        cafe_preference_rate = self.cleaned_data['cafe_preference_rate']
        viewpoints_preference_rate = self.cleaned_data['viewpoints_preference_rate']
        monument_preference_rate = self.cleaned_data['monument_preference_rate']
        
        print("New trip survey responses for user {} : {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            																	user,
                             													religious_place_preference_rate,
																				parks_preference_rate,
																				theaters_preference_rate,
																				mall_preference_rate,
																				museum_preference_rate,
																				art_gallery_preference_rate,
																				zoo_preference_rate,
																				restaurant_preference_rate,
																				pubs_preference_rate,
																				gym_preference_rate,
																				spa_preference_rate,
																				cafe_preference_rate,
																				viewpoints_preference_rate,
																				monument_preference_rate))

  
    def save_survey(self, user_id):     
        
        new_trip_survey = TripSurvey(
			rate_of_religious_place = self.cleaned_data['religious_place_preference_rate'],
			rate_of_parks = self.cleaned_data['parks_preference_rate'],
			rate_of_theaters = self.cleaned_data['theaters_preference_rate'],
			rate_of_mall = self.cleaned_data['mall_preference_rate'],
			rate_of_museum = self.cleaned_data['museum_preference_rate'],
			rate_of_art_gallery = self.cleaned_data['art_gallery_preference_rate'],
			rate_of_zoo = self.cleaned_data['zoo_preference_rate'],
			rate_of_restaurant = self.cleaned_data['restaurant_preference_rate'],
			rate_of_pubs = self.cleaned_data['pubs_preference_rate'],
			rate_of_gym = self.cleaned_data['gym_preference_rate'],
			rate_of_spa = self.cleaned_data['spa_preference_rate'],
			rate_of_cafe = self.cleaned_data['cafe_preference_rate'],
			rate_of_viewpoints = self.cleaned_data['viewpoints_preference_rate'],
			rate_of_monument = self.cleaned_data['monument_preference_rate']
        ).insert_new_instance(user_id)
        
        PersonalInfo().set_trip_survey_in_info(user_id, new_trip_survey)

        print("New trip survey created")
