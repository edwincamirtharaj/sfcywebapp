# company/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import os
from datetime import datetime

class WhatsAppNumber(models.Model):
    number = models.CharField(max_length=15)
    companies = models.ManyToManyField('Company', related_name='whatsapp_numbers')

    def __str__(self):
        return self.number

class Company(models.Model):
    name = models.CharField(max_length=255)
    pan_number = models.CharField(max_length=10, unique=True, error_messages={'unique': 'This PAN is already in use.'})
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    email = models.EmailField()
    is_approved = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=32, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=10)

    def generate_confirmation_token(self):
        return get_random_string(length=32)

    def save(self, *args, **kwargs):
        if not self.confirmation_token:
            self.confirmation_token = self.generate_confirmation_token()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserCompanyMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_user_verified = models.BooleanField(default=False)  # New field for user verification
    is_approved = models.BooleanField(default=True)
    verification_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

class Year(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)


class Month(models.Model):
    month = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.month


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    show_field = models.BooleanField(default=True)  # Added BooleanField

    def __str__(self):
        return self.name


class ReportName(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    show_field = models.BooleanField(default=True)  # Added BooleanField

    def __str__(self):
        return f"{self.name} - {self.department}"



class FileUpload(models.Model):

    def dynamic_upload_path(self, filename):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f'uploads/{self.company_id}/{self.department}/{self.year}/{self.month}/{str(self.reports_name)}/{timestamp}_{filename}'

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    reports_name = models.ForeignKey(ReportName, on_delete=models.CASCADE)
    file = models.FileField(upload_to=dynamic_upload_path)
    upload_date = models.DateField(auto_now_add=True)
    file_name = models.CharField(max_length=255)  # taken from uploaded file name
    description = models.TextField()
    show_field = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    extra_field1 = models.CharField(max_length=255, blank=True, null=True)
    extra_field2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.file_name} - {self.company} - {self.department}"

    def save(self, *args, **kwargs):
        # Set the file name to the original filename
        self.file_name = os.path.basename(self.file.name)

        # Create the company directory if it doesn't exist
        company_dir = f'uploads/company_{self.company_id}'
        os.makedirs(company_dir, exist_ok=True)

        # Create the department directory if it doesn't exist
        department_dir = f'{company_dir}/{self.department}'
        os.makedirs(department_dir, exist_ok=True)

        # Create the year directory if it doesn't exist
        year_dir = f'{department_dir}/{self.year}'
        os.makedirs(year_dir, exist_ok=True)

        # Create the month directory if it doesn't exist
        month_dir = f'{year_dir}/{self.month}'
        os.makedirs(month_dir, exist_ok=True)

        # Create the reportname directory if it doesn't exist
        reportname_dir = f'{month_dir}/{str(self.reports_name)}'
        os.makedirs(reportname_dir, exist_ok=True)

        super().save(*args, **kwargs)