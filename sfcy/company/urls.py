# company/urls.py
from django.urls import path
from .views import CompanyCreateView, VerifyUserMappingView, user_mapping, company_dashboard, CompanyFilesView, access_denied

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('user_mapping/', user_mapping, name='user_mapping'),
    path('verify_user_mapping/<int:mapping_id>/<str:verification_token>/', VerifyUserMappingView.as_view(), name='verify_user_mapping'),
    path('company_dashboard/<int:company_id>/', company_dashboard, name='company_dashboard'),
    path('<int:company_id>/files/', CompanyFilesView.as_view(), name='company_files'),
    path('access-denied/', access_denied, name='access_denied'),

]
