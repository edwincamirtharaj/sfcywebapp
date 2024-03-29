# company/views.py
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from .models import Company, WhatsAppNumber, UserCompanyMapping, FileUpload
from .forms import CompanyForm, CompanyMappingForm, FileUploadForm
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@method_decorator(login_required, name='dispatch')
class CompanyCreateView(View):
    def get(self, request):
        form = CompanyForm()
        return render(request, 'company/company_create.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)


            # Get WhatsApp number from the form

            whatsapp_number = form.cleaned_data['whatsapp_number']

            company.save()

            # Create or get the WhatsappNumber instance and associate it with the company
            whatsapp_number_instance, created = WhatsAppNumber.objects.get_or_create(number=whatsapp_number)
            whatsapp_number_instance.companies.add(company)

            # Create UserCompanyMapping for the authenticated user and the created company
            user_company_mapping = UserCompanyMapping.objects.create(user=request.user, company=company)

            # Generate a verification token for user mapping
            verification_token = get_random_string(length=32)
            user_company_mapping.verification_token = verification_token
            user_company_mapping.save()

            # Send confirmation email to the company owner with user mapping verification link
            verification_link = f"http://www.sfcy.in/company/verify_user_mapping/{user_company_mapping.id}/{verification_token}/"
            subject = 'Company Confirmation'
            print(verification_link)
            message = render_to_string('company/confirmation_email.html', {'company': company, 'verification_link': verification_link})
            #plain_message = strip_tags(message)
            from_email = 'webappbook@gmail.com'  # Update with your email or use a custom sender
            to_email = company.email


            email = EmailMessage(subject, message, from_email, [to_email])
            email.content_subtype = 'html'
            email.send()

            return redirect('account_profile')

        return render(request, 'company/company_create.html', {'form': form})

class VerifyUserMappingView(View):
    def get(self, request, mapping_id, verification_token):
        user_company_mapping = get_object_or_404(UserCompanyMapping, id=mapping_id, verification_token=verification_token)

        # Verify the user mapping
        user_company_mapping.is_user_verified = True
        user_company_mapping.save()

        # Redirect to a success page or display a success message
        return render(request, 'company/user_mapping_verified.html')


def user_mapping(request):
    if request.method == 'POST':
        form = CompanyMappingForm(request.POST)
        if form.is_valid():
            pan_number = form.cleaned_data['pan_number']

            try:
                company = Company.objects.get(pan_number=pan_number)
                if UserCompanyMapping.objects.filter(user=request.user, company=company).exists():
                        messages.warning(request, 'You are already linked to this company.')
                        return redirect('user_mapping')
                else:
                    # Create UserCompanyMapping for the authenticated user
                    user_company_mapping = UserCompanyMapping.objects.create(user=request.user, company=company)

                    # Generate a verification token for user mapping
                    verification_token = get_random_string(length=32)
                    user_company_mapping.verification_token = verification_token
                    user_company_mapping.save()

                    # Send confirmation email to the company owner with user mapping verification link
                    verification_link = f"http://www.sfcy.in/company/verify_user_mapping/{user_company_mapping.id}/{verification_token}/"
                    subject = 'User Confirmation'
                    username = request.user.username
                    message = render_to_string('company/confirmation_email.html', {'company': company, 'verification_link': verification_link, 'subject':subject, 'username':username})

                    from_email = 'webappbook@gmail.com'  # Update with your email or use a custom sender
                    to_email = company.email


                    email = EmailMessage(subject, message, from_email, [to_email])
                    email.content_subtype = 'html'
                    email.send()

                return redirect('account_profile')


            except Company.DoesNotExist:
                messages.error(request, 'Company with this PAN number does not exist.')
                return redirect('user_mapping')


    else:
        form = CompanyMappingForm()

    return render(request, 'company/user_mapping.html', {'form': form})

def company_dashboard(request, company_id):
    # Get the company based on the provided company_id
    company = get_object_or_404(Company, id=company_id)

    # Check if the user is a staff member
    if request.user.is_staff:
        # If user is staff, allow access without checking user_mapping
        pass
    else:
        user_mapping = UserCompanyMapping.objects.filter(user=request.user, company=company, is_user_verified=True, is_approved=True).first()
        if user_mapping is None:
            # Redirect to another page or display an error message
            return redirect('access_denied')

    # Pass relevant data to the template
    context = {
        'company': company,
    }

    return render(request, 'company/company_dashboard.html', context)

class CompanyFilesView(View):
    template_name = 'company/company_files.html'
    form_class = FileUploadForm
    items_per_page = 9

    def get(self, request, company_id):
        # Get the company data based on company_id
        company = get_object_or_404(Company, id=company_id)

        # Retrieve files associated with the company
        files = FileUpload.objects.filter(company=company).order_by('-id')

        # Paginate the files
        paginator = Paginator(files, self.items_per_page)
        page = request.GET.get('page')

        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            files = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            files = paginator.page(paginator.num_pages)

        # Initialize the form for file uploads
        form = self.form_class(initial={'company': company})

        context = {'company': company, 'files':files, 'form':form}
        return render(request, self.template_name, context)

    def post(self, request, company_id):
        # Get the company data based on company_id
        company = get_object_or_404(Company, id=company_id)

        # Retrieve files associated with the company
        files = FileUpload.objects.filter(company=company)

        # Handle file upload
        form = self.form_class(request.POST, request.FILES, initial={'company': company})

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.company = company  # Set the company for the uploaded file
            instance.save()

            messages.success(request, 'File uploaded successfully.')
            return redirect('company_files', company_id=company.id)

        # If the form is not valid, re-render the page with the form and files
        context = {'company': company, 'files': files, 'form': form}
        return render(request, self.template_name, context)


def access_denied(request):
    return render(request, 'company/access_denied.html')

