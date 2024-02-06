from django.contrib import admin
from .models import WhatsAppNumber, Company, UserCompanyMapping, Year, Month, Department, ReportName, FileUpload
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Unregister the existing UserAdmin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')  # Customize the fields displayed in the list view
    list_editable = ('is_active', 'is_staff', 'is_superuser')  # Enable editing for the 'is_active' field directly in the list view

@admin.register(WhatsAppNumber)
class WhatsAppNumberAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'pan_number', 'is_approved', 'confirmation_token', 'whatsapp_number')

@admin.register(UserCompanyMapping)
class UserCompanyMappingAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'is_user_verified', 'is_approved', 'verification_token')
    list_editable = ('is_user_verified','is_approved')

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year',)

@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('month',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_field')

@admin.register(ReportName)
class ReportNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'show_field')

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'company', 'department', 'upload_date', 'is_verified')
