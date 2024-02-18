from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from surveys.forms import BaseSurveyForm
from .models import PersonalInfo


def set_text_input():
        return forms.TextInput(attrs={'class':'form-control'})

class PersonalInfoForm(BaseSurveyForm):
	
        city = forms.CharField(label='City',
                                help_text=mark_safe("<p>info must longer than five</p>"),   
                                widget=set_text_input())
        distinct = forms.CharField(label='Distinct',
                                help_text=mark_safe("<p>info must longer than five</p>"),   
                                widget=set_text_input())
        neighbor = forms.CharField(label='neighbor',
                                help_text=mark_safe("<p>info must longer than five</p>"),   
                                widget=set_text_input())
        other_addr_infos = forms.CharField(label='Address', 
                                help_text=mark_safe("<p>info must longer than five</p>"),   
                                widget= forms.Textarea(attrs={'class':'form-control'}))
        cell_phone_no = forms.CharField(label='Phone No',  
                                help_text=mark_safe("""<p>info must longer than five</p>
                                                    <p>exp : 123-456-78-90</p>"""),       
                                widget= Input(attrs={
                                'type':'tel',
                                'class':'form-control',
                                'placeholder': '123-45-678'
                                }))
 
        def show_infos(self,user_id):
                
                city = self.cleaned_data['city']
                distinct = self.cleaned_data['distinct']
                neighbor = self.cleaned_data['neighbor']
                other_addr_infos = self.cleaned_data['other_addr_infos']
                cell_phone_no = self.cleaned_data['cell_phone_no']
                user = User.objects.get(id = user_id)

                print("""New Personal Survey Responses for user {} : {}, {}, {} , {}, {}""".format(user,
                                                                                        city,
                                                                                        distinct,
                                                                                        neighbor,
                                                                                        other_addr_infos,
                                                                                        cell_phone_no))
                
        def save_survey(self, user_id):
                
                new_personal_survey = PersonalInfo(
                                city = self.cleaned_data['city'],
                                distinct = self.cleaned_data['distinct'],
                                neighbor = self.cleaned_data['neighbor'],
                                other_addr_infos = self.cleaned_data['other_addr_infos'],
                                cell_no = self.cleaned_data['cell_phone_no'],
                        ).set_other_field_im_infos(user_id)
                
                print("Fields other than survey infos are saved in personal info {}".format(new_personal_survey))
                
        def update_survey(self, user_id):
                
                new_personal_survey = PersonalInfo(
                                city = self.cleaned_data['city'],
                                distinct = self.cleaned_data['distinct'],
                                neighbor = self.cleaned_data['neighbor'],
                                other_addr_infos = self.cleaned_data['other_addr_infos'],
                                cell_no = self.cleaned_data['cell_phone_no'],
                        ).set_other_field_im_infos(user_id)
                
                print("Fields other than survey infos are saved in personal info {}".format(new_personal_survey))
 

class Counter:

        def __init__(self,number):
                self.count=number

        def increase_counter(self):
                self.count+=1
                return self.count