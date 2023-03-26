
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from login.models import userProfileAdmin, WaitingRoom
from medical.forms import AddHospital
import re
from django.core.validators import validate_email, EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError


def customPasswordValidator(password1,password2):

    if password1 == password2:
        return False
    return True

class WaitingRoomForm(AddHospital):
    email = forms.EmailField(label="Email(used to send confirmation link)",max_length=50, min_length=7,required=True,validators=[EmailValidator(message="Please input the Email in the Proper format")])
    class Meta:
        model = WaitingRoom
        fields = ['id','email' ,'name','taxid','bankaccount','routing','street','city','state','zip', 'website','total_physicians']


class UserProfileAdminForm(ModelForm):

    class Meta:
        model = userProfileAdmin
        exclude = ['user']
    
    def clean_mobile_contact(self):
        mobile_contact = self.cleaned_data.get('mobile_contact','')
        result = re.match(pattern=r'^\d{3}-?\d{3}-?\d{4}$',string=mobile_contact)
        if not result:
            raise ValidationError("Invalid Format.The Mobile Contact Number should be a 10 digit number in the format ###-###-#### (Dashes are optional)")
        if "-" in mobile_contact:
            mobile_contact = "".join(mobile_contact.split('-'))
        
        return mobile_contact

class Login(forms.Form):
    username = forms.CharField(required=True, label="Username", widget=forms.TextInput(attrs={'placeholder':'Please enter a username','required':True,
    'required':'true','name':'email'}), validators=[])
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Please enter a password.','required':True,'required':'true'}))
    class Meta:
        pass

class ForgotLogin(forms.Form):
    email = forms.CharField(required=True, label="Email", widget=forms.TextInput(attrs={'placeholder':'Please enter a username','required':True,
    'required':'true','name':'email'}), validators=[EmailValidator(message="Please enter an email in the valid format.")])
    
class ResetPassword(forms.Form):
        password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Please enter a password.','required':True,'required':'true'}))
        password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Please enter a password.','required':True,'required':'true'}))

        def clean_password2(self,*args,**kwargs):
            password1 = self.cleaned_data.get('password1', False)
            password2 = self.cleaned_data.get('password2', False)

            if password1 and password2:
                password_validate_result = customPasswordValidator(password1=password1,password2=password2)

                if password_validate_result:
                    raise ValidationError("Please Input a Matching Password with the minimum complexity requirements.")

                result = re.match(pattern=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,16}$',string=password2)
                if not result:
                    raise ValidationError("Password must be a Minimum eight to sixteen characters, at least one letter and one number")

            return password2



