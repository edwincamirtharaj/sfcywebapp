# views.py - Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from company.models import Company, WhatsAppNumber, UserCompanyMapping

@login_required
def profile(request):
   # Get the UserCompanyMapping instances for the current user
    user_mappings = UserCompanyMapping.objects.filter(user=request.user)

    # Extract the associated companies' names
    companies = [user_mapping.company for user_mapping in user_mappings]
    context = {'user': request.user, 'companies': companies}
    return render(request, 'account/profile.html', context)
