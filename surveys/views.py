
from .models import PersonalSurvey, AccommodateSurvey, TripSurvey
from .forms import PersonalSurveyForm, AccommodateSurveyForm, TripSurveyForm, BaseSurveyForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def personal_survey_view(request):
    
    return set_last_template(request = request,
							survey_title = "Personal Questions", 
                      		brief_description = None,
                      		form_template = PersonalSurveyForm,
                      		redirect_name = 'surveys:newAccommodateSurvey')


@login_required
def accommodate_survey_view(request):
    
    
    return set_last_template(request = request,
							survey_title = "Accommodate Questions", 
                      		brief_description = None,
                      		form_template = AccommodateSurveyForm,
                      		redirect_name = 'surveys:newTripSurvey')


@login_required
def trip_survey_view(request):
	
    return set_last_template(request,
                      survey_title = "Trip Questions",
                      brief_description = "Give rate value to every trip place for your preference",
                      form_template = TripSurveyForm,
                      redirect_name = 'person:personInfoEnter')
    

def set_last_template(request,
                    survey_title,
                    is_edit = False,
                    brief_description = None,
                    pre_form_template = None,
                    form_template = BaseSurveyForm,
                    redirect_name='page',
                    template_name = "surveys/survey_template.html"):

	if not request.session.has_key('user_id'):
		return render (request=request, template_name="personal_info/user_not_found.html")

	# for field in AccommodateSurveyForm():
	# 	field.name
	user_id = request.session['user_id']
	haveError = False
	form = None
	if request.method == "POST":
		form = form_template(request.POST)
		if form.is_valid():
			form.show_infos(user_id)
			form.save_survey(user_id)
			return redirect(redirect_name)
		else:
			haveError = True
	
	if not is_edit:
		if not haveError:
			form = form_template()
		else:
			if form is not None:
				for field in form:
					for error in field.errors:
						print(error)
	else:
		form = pre_form_template
	context = {"form" : form, "title": survey_title}
	if brief_description is not None: 
		context['brief_description'] = brief_description
	return render (request=request, template_name=template_name,context=context)

