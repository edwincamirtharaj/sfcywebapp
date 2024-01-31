# company/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, WhatsAppNumber, UserCompanyMapping

class UserCompanyMappingForm(forms.ModelForm):
    class Meta:
        model = UserCompanyMapping
        fields = ['company', 'is_approved']

class CompanyForm(forms.ModelForm):
    whatsapp_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = Company
        exclude = ['is_approved', 'confirmation_token']  
        
class CompanyMappingForm(forms.Form):
    pan_number = forms.CharField(label='Company PAN Number', max_length=10)
