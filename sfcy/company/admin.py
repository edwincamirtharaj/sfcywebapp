from django.contrib import admin
from .models import WhatsAppNumber, Company, UserCompanyMapping, Year, Month, Department, ReportName, FileUpload

@admin.register(WhatsAppNumber)
class WhatsAppNumberAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'pan_number', 'is_approved', 'confirmation_token', 'whatsapp_number')

@admin.register(UserCompanyMapping)
class UserCompanyMappingAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'is_user_verified', 'is_approved', 'verification_token')

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
