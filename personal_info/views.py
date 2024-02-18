import random
import json
from .forms import Counter, PersonalInfoForm
from .models import PersonalInfo
from django.db.models import Model
from surveys.models import PersonalSurvey, AccommodateSurvey, TripSurvey
from utils.models import *
from surveys.forms import PersonalSurveyForm, AccommodateSurveyForm ,TripSurveyForm, BaseSurveyForm
from surveys.views import set_last_template
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator

testList = []
for i in range(15):
    testList.append({'name': 'test{}'.format(i) , 'star': random.randint(0,5)})

def get_survey_values_as_dictionary(survey_object):
    
    
    not_shown_fields = ['id', 'user_id' ] 
    model_field_name_list = [ field.name for field in survey_object._meta.get_fields() if field.name not in not_shown_fields ]
    field_size = len(model_field_name_list)
    
    model_field_class_list = [ 
                                (model_field_name, getattr(survey_object, model_field_name).__class__.__name__)
                                for model_field_name in model_field_name_list]
    model_field_value_list = [ ]
    model_field_label_dict = {}
    for model_field_class in model_field_class_list:
        if model_field_class[1] in ['int', 'str', 'float']:
            model_field_value_list.append(getattr(survey_object, model_field_class[0]))
        elif model_field_class[0] == 'amenities':
            amenities = []
            amenities_labels = []
            for amenity_object in  getattr(survey_object, model_field_class[0]).all():
                amenities.append(amenity_object.type)
                amenities_labels.append(amenity_object.label)
                
            model_field_value_list.append(amenities)
            model_field_label_dict['amenities'] = amenities_labels
        else :
            model_field_key =  model_field_class[0]
            model_field_value = getattr(survey_object, model_field_key)
            model_field_value_list.append(str(model_field_value.type))
            model_field_label_dict[model_field_key] = model_field_value.label
            
    result_list = []
    for i in range(field_size):
        key = model_field_name_list[i]
        result_elm = {
            "key": key,
            "value": model_field_value_list[i]
        }
        
        if key in model_field_label_dict.keys() :
            result_elm['label'] = model_field_label_dict[key]
        
        result_list.append(result_elm)
    
    
    return result_list
    
    

@login_required
def view_personal_infos(request):

    return set_last_template(request,
                            "Personal Info Form", 
                            brief_description = None,
                            form_template = PersonalInfoForm,
                            redirect_name = 'person:personDashboard',
                            template_name = 'personal_info/personal_info_edit.html')

@login_required
def view_personal_dashboard(request):
    if not request.session.has_key('user_id'):
        return render (request=request, template_name="personal_info/user_not_found.html")

    return render (request=request, template_name="personal_info/person_dashboard.html")

@login_required
def view_personal_settings(request):
    if not request.session.has_key('user_id'):
        return render (request=request, template_name="personal_info/user_not_found.html")

    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    personal_info = PersonalInfo.objects.filter(user_id = user).get()
    context = {
            "personal_infos" : personal_info,
            "settings_form": PersonalInfoForm(),
            "settings_title": 'Personal Info Form'
    }
    return render (request=request, template_name="personal_info/person_settings.html", context=context)


@login_required
def view_survey_infos(request):
    if not request.session.has_key('user_id'):
        return render (request=request, template_name="personal_info/user_not_found.html")

    #get surevy infos
    the_survey_details = []
    the_survey_details.append({
        "survey_id": "personal_survey_div",
        "survey_name": "Personal Survey", 
        "survey_form": PersonalSurveyForm()
    })
    the_survey_details.append({
        "survey_id": "accommodate_survey_div", 
        "survey_name": "Accommodate Survey", 
        "survey_form": AccommodateSurveyForm()
    })
    the_survey_details.append({
        "survey_id": "trip_survey_div", 
        "survey_name": "Trip Survey", 
        "survey_form": TripSurveyForm()
    })
    button_infos = [{"id": "personal_survey_div", "name" : "Personal Survey","type": "info"},
                    {"id": "accommodate_survey_div", "name" : "Accommodate Survey","type": "warning"},
                    {"id": "trip_survey_div", "name" : "Trip Survey","type": "success"}]
    
    context = {"the_survey_details": the_survey_details, "button_infos": button_infos}
    return render (request=request  , template_name="personal_info/person_survey_infos.html",context=context)


def get_survey_infos(request):

    user_id = request.session['user_id']
    
    user = User.objects.get(id = user_id)
    user_personal_info = PersonalInfo.objects.filter(user_id = user).get()
    personal_survey_dict = get_survey_values_as_dictionary(user_personal_info.personal_survey_id)
    accommodate_survey_dict = get_survey_values_as_dictionary(user_personal_info.accommodate_survey_id)
    trip_survey_dict = get_survey_values_as_dictionary(user_personal_info.trip_survey_id)
    
    for trip_survey in trip_survey_dict:
        trip_survey_key = trip_survey['key']
        trip_survey_key_keywords = trip_survey_key.split("_")
        trip_survey['key'] = trip_survey_key_keywords[2] + "_preference_" + trip_survey_key_keywords[0]
    
    context = {
        "survey_infos":[{ "div_id":"personal_survey_div", "keys_and_values" : personal_survey_dict},
                        { "div_id":"accommodate_survey_div", "keys_and_values" : accommodate_survey_dict},
                        { "div_id":"trip_survey_div", "keys_and_values" : trip_survey_dict}]
    }
    
    return JsonResponse(context)


@csrf_exempt
def edit_survey_infos(request):
    
    json_data = {}
    user_id = request.session['user_id']
        
    try:
    
        if user_id != -1:
            body_json = json.loads(request.body.decode())
            survey_div_id = body_json['div_id']
            form_datas = {}
            keys_and_values = body_json['keys_and_values']
            for keys_and_value in keys_and_values:
                form_datas[keys_and_value['key']] = keys_and_value['value']
            
            new_survey = BaseSurveyForm()
            if survey_div_id.startswith('personal_survey'):
                new_survey = PersonalSurveyForm(form_datas)
            elif survey_div_id.startswith('accommodate_survey'):
                new_survey = AccommodateSurveyForm(form_datas)
            elif survey_div_id.startswith('trip_survey'):
                new_survey = TripSurveyForm(form_datas)
            
            if new_survey == None :
                json_data['message'] = 'form object not found'
                return JsonResponse(json_data)
            
            
            if new_survey.is_valid():
                new_survey.save_survey(user_id)
            else :
                json_data['message'] = 'form is not valid'
                return JsonResponse(json_data)
                
            json_data['message'] = "Successfully saved"
    
    except Exception as e:
        print(e.__traceback__)
        json_data['message'] = 'failed' 
                
    return JsonResponse(json_data)


@csrf_exempt
def edit_personal_infos(request):
    
    
    json_data = {}
    user_id = request.session['user_id']
        
    try:
    
        if user_id != -1:
            form_datas = json.loads(request.body.decode())
            
            form_datas['email'] = None
            new_personal_info = PersonalInfoForm(form_datas)
            
            if new_personal_info.is_valid():
                new_personal_info.save_survey(user_id)
            else :
                json_data['message'] = 'form is not valid'
                return JsonResponse(json_data)
                
            json_data['message'] = "Successfully saved"
    
    except Exception as e:
        print(e.__traceback__)
        json_data['message'] = 'failed' 
                
    return JsonResponse(json_data)


@login_required
def view_and_edit_travel_calender(request):
    return render(request=request, template_name="personal_info/person_calender.html")
    
