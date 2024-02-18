
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.http import Http404
from personal_info.models import PersonalInfo



#User = settings.AUTH_USER_MODEL


endpoint_method_list = {
	"get-list": "POST",
	"set-rate": "POST",
	"edit_survey_infos": "POST",
	"new-survey-responses": "POST",
	"add-plan-to-calender": "POST",
	"set-rate": "POST",
	"set-all-host-trip-plan": "POST",
	"get-host-trip-plan" : "GET",
	"get-photo-urls" : "GET",
	"transfer-data" : "GET",
	"get-all-rates" : "GET",
	"get-survey-responses" : "GET",
	"get-all-rates" : "GET",
	"get-plans" : "GET",
 	"remove-plan-from-calender" : "DELETE"
}


class UserOperations:

	def is_user_exist(self, user_id):
		return User.objects.filter(id = user_id).exists()
  
	def set_user_activation(id):
		try:
			User.objects.filter(id=id).update(is_active=True)
		except Exception as e:
			print("Failed to activate user : " + str(e))
			return False
		return True

	def create_personal_info(self, user):
		
		personal_info_instance = PersonalInfo(user_id = user)
		personal_infos = personal_info_instance.get_personal_info_by_user_ref()
		try:
			if len(personal_infos) == 0:
				personal_infos = personal_info_instance.save_personal_info()
			else:
				return "person:personDashboard"
		except Exception as e:
			print("Failed to activate user : " + str(e))
			return None
		return "enters:postEnter"


class SessionControllerMiddleware(object):
    
	def __init__(self, get_response):
        
		self.get_response = get_response
	
	def __call__(self, request):
		
		pathlist = request.path_info.split('/')
		if len(pathlist) >= 3:
			last_path = pathlist[2]
			if last_path in endpoint_method_list.keys() :
				if endpoint_method_list[last_path] != request.method:
					response = HttpResponse(json.dumps({'message': 'This endpoint only allow POST request'}), 
                                content_type='application/json')
					response.status_code = 400
					return response
  
		if not request.path_info.startswith('/register') or not request.path_info.endswith('set-all-host-trip-plan') or not request.path_info.endswith('transfer-data'):
			
			if 'user_id' in request.session.keys():
				
				user_id = request.session['user_id']
				if not UserOperations().is_user_exist(user_id=user_id) :
					return HttpResponseForbidden(json.dumps({ 'message': 'user not found'}), 
                                content_type='application/json')	
			else:
				user_id = request.META['HTTP_USERID']

				if user_id == -1 or user_id == None:
					return HttpResponseForbidden(json.dumps({ 'message': 'user_id not found'}), 
                                content_type='application/json')	
				else:
					request.session['user_id'] = user_id
					if not UserOperations().is_user_exist(user_id=user_id) :
						return HttpResponseForbidden(json.dumps({ 'message': 'user not found'}), 
                                content_type='application/json')	
		

		response = self.get_response(request)
		return response

    
