# company/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

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
    is_approved = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"