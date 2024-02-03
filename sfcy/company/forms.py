# company/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, WhatsAppNumber, UserCompanyMapping, FileUpload, ReportName, Department, Month, Year, ReportName

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

class FileUploadForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        label='Department',
        queryset=Department.objects.all(),  # Set the queryset to get all departments
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    month = forms.ModelChoiceField(
        label='Month',
        queryset=Month.objects.all(),  # Set the queryset to get all departments
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    year = forms.ModelChoiceField(
        label='Year',
        queryset=Year.objects.all(),  # Set the queryset to get all departments
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    reports_name = forms.ModelChoiceField(
        label='Report',
        queryset=ReportName.objects.all(),  # Set the queryset to get all departments
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        label='Remarks',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf,image/*'}),
    )

    class Meta:
        model = FileUpload
        fields = ['department', 'month', 'year', 'reports_name','description', 'file']
