from django.db import models
from django.contrib.auth.models import User
from surveys.models import PersonalSurvey, AccommodateSurvey, TripSurvey


class PersonalInfo(models.Model):
    
	id = models.AutoField(unique=True,primary_key=True,auto_created=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
	#is_first_login = models.BooleanField(default=True, blank=True, null=True)
	city = models.CharField(max_length=20, default=None, blank=True, null=True)
	distinct = models.CharField(max_length=20, default=None, blank=True, null=True)
	neighbor = models.CharField(max_length=20, default=None, blank=True, null=True)
	# longitude = models.CharField(max_length=20, default=None, blank=True, null=True)
	# latitude = models.CharField(max_length=20, default=None, blank=True, null=True)
	other_addr_infos = models.CharField(max_length=100, default=None, blank=True, null=True)
	cell_no = models.CharField(max_length=15, default=None, blank=True, null=True)
	personal_survey_id = models.ForeignKey(PersonalSurvey, on_delete=models.CASCADE,related_name='+', default=None, blank=True, null=True)
	accommodate_survey_id = models.ForeignKey(AccommodateSurvey, on_delete=models.CASCADE,related_name='+', default=None, blank=True, null=True)
	trip_survey_id = models.ForeignKey(TripSurvey, on_delete=models.CASCADE,related_name='+', default=None, blank=True, null=True)
	#calenderPlans = models.ManyToManyField(TripPlan, related_name='+', default=None, blank=True, null=True)
 
	def set_other_field_im_infos(self, user_id):
		
		user = User.objects.get(id = user_id)
		PersonalInfo.objects.filter(user_id = user).update(city =  self.city,
																		distinct =  self.distinct,
																		neighbor =  self.neighbor,
																		other_addr_infos =  self.other_addr_infos,
																		cell_no =  self.cell_no)

 
	def set_personal_survey_in_info(self, user_id, personal_survey):
     
		user = User.objects.get(id = user_id)
		PersonalInfo.objects.filter(user_id = user).update(personal_survey_id = personal_survey)
  
   
	def set_accommodate_survey_in_info(self, user_id, accommodate_survey):
     
		user = User.objects.get(id = user_id)
		PersonalInfo.objects.filter(user_id = user).update(accommodate_survey_id = accommodate_survey)
  
   
	def set_trip_survey_in_info(self, user_id, trip_survey):
     
		user = User.objects.get(id = user_id)
		PersonalInfo.objects.filter(user_id = user).update(trip_survey_id = trip_survey)
  
  
	def get_personal_info_by_id(self):
		personal_info = PersonalInfo.objects.get(id = self.id)
		return personal_info

	def get_personal_info_by_user_ref(self):
		personal_infos = PersonalInfo.objects.filter(user_id = self.user_id).all()
		return personal_infos

	def save_personal_info(self):

		new_personal_info = PersonalInfo.objects.create(
											user_id = self.user_id
											#calenderPlans = self.calenderPlans
										)

		print("Personal info created ".format(new_personal_info))
	
		return new_personal_info

	def isFieldsNull(self):
		
		is_null = 0;
		for field in self.__dict__:
			if self.__dict__[field] == '':
				is_null += 1
		
		return is_null > 0

