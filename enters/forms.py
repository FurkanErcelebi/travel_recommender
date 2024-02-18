from django import forms  
from django.conf import settings
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.core.mail import send_mail
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  
from django.utils.html import strip_tags
from django.template.loader import render_to_string
  
class SignUpForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150
    	,widget=forms.TextInput(
    	attrs={
        'class': 'form-control signInInputs',
        'placeholder': 'username',
        'id': 'username'
        })
        )
    email = forms.EmailField(label='email'
    	, widget=forms.TextInput(
        attrs={
        'class': 'form-control signInInputs',
        'placeholder': 'exp: some_email@gmail',
        })
        )  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
        'class': 'form-control signInInputs',
        'id': 'password1'
        }))  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={
        'class': 'form-control signInInputs',
        'id': 'password2'
        }))  

    class Meta:
       model = User
       fields = ('username', 'email', 'password1', 'password2')
    #    labels={
    #        "username": "custom label for username"
    #    }
    #    error_messages={
    #        "username": {
    #            "required": "custom message for required"
    #         }
    #    }


    def sendLink(self, user):
        email = user.email
        id1 = user.id
        html_message = render_to_string('enters/activate_message.html', {'id': id1})
        plain_message = strip_tags(html_message)
        print(html_message)
        send_mail(
                subject='Travel Recommend Welcome',
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message)


    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    # def clean_password2(self):  
    #     password1 = self.cleaned_data['password1']  
    #     password2 = self.cleaned_data['password2']  
    #     print('{} : {}'.format(password1, password2))
  
    #     if password1 and password2 and password1 != password2:  
    #         raise ValidationError("Password don't match")  
    #     return password2

  
    def save(self, commit = True):  
        user = User.objects.create_user(
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )
        
        User.objects.filter(id=user.id).update(is_active=False)
        return user
 # type: ignore        return user



#Look later
class LoginFormV1(AuthenticationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150
    	,widget=forms.TextInput(
    	attrs={
        'class': 'form-control signInInputs',
        'placeholder': 'username',
        })
        )

    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
        'class': 'form-control signInInputs',
        })) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={ 'class': 'form-control'})
        self.fields['password'].widget = forms.widgets.PasswordInput(attrs={ 'class': 'form-control'})

    #class Meta:
    #   model = User
    #   fields = ('username', 'password')
    #    labels={
    #        "username": "custom label for username"
    #    }
    #    error_messages={
    #        "username": {
    #            "required": "custom message for required"
    #         }
    #    }

    # def authenticateUser(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     print("{} : {}".format(username, password))
    #     # user = authenticate(username=username, password=password)
    #     # return user

    # def username_clean(self):  
    #     username = self.cleaned_data['username'].lower()  
    #     new = User.objects.filter(username=username)  
    #     if new.count() == 0:  
    #         new = User.objects.filter(email=username)  
    #         if new.count() == 0:  
    #             raise ValidationError("User not Exist")  
    #     return username
  
    # def clean_password(self):  
    #     password1 = self.cleaned_data['password']
  
    #     if password1 and password2 and password1 != password2:  
    #         raise ValidationError("Password don't match")  
    #     return password2 

class LoginForm(Form):

    username = forms.CharField(label='username', min_length=5, max_length=150
    	,widget=forms.TextInput(
    	attrs={
        'class': 'form-control signInInputs',
        'placeholder': 'username',
        }), required=True
        )

    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
        'class': 'form-control signInInputs',
        }), required=True
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username = username)  
        if not user:  
            raise forms.ValidationError("User not Exist") 
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        return user

     # add validation for username