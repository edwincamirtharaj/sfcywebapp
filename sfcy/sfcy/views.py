# views.py - Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from company.models import Company, WhatsAppNumber, UserCompanyMapping

@login_required
def profile(request):
    # Get the UserCompanyMapping instances for the current user
    if request.user.is_staff:
        # If user is staff, show all company details
        user_mappings = UserCompanyMapping.objects.all()
    else:
        # Get the UserCompanyMapping instances for the current user
        user_mappings = UserCompanyMapping.objects.filter(user=request.user, is_user_verified=True, is_approved=True)

    # Extract the associated companies' names
    #company_names = [user_mapping.company.name for user_mapping in user_mappings]
    companies_set = set(user_mapping.company for user_mapping in user_mappings)
    companies = list(companies_set)
    context = {'user': request.user, 'companies': companies}
    return render(request, 'account/profile.html', context)
