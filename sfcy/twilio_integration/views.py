# views.py
from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client
from company.models import WhatsAppNumber

from django.http import HttpRequest, HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt

def success_view(request):
    return render(request, 'twilio_integration/success.html')

@csrf_exempt
def handle_whatsapp_message(request: HttpRequest):
    # Extract data from Twilio request
    incoming_message = request.POST.get('Body', '')
    sender_whatsapp_number = request.POST.get('From', '')

    cleaned_number = ''.join(c for c in sender_whatsapp_number if c.isdigit())[2:]
    try:
        whatsapp_number = WhatsAppNumber.objects.get(number=cleaned_number)
        associated_companies = whatsapp_number.companies.all()

        # Check if the user is associated with any companies
        if associated_companies.exists():
            # Prompt the user with their company list
            menu_message = "Select your company:\n"
            for index, company in enumerate(associated_companies, start=1):
                menu_message += f"{index}. {company.name}\n"
                if index < len(associated_companies):
                    menu_message += "_____________________\n"

            # Add a prompt asking the user to reply with the number corresponding to their company
            menu_message += "____________________________________"

            # Send the company list as a reply
            response = MessagingResponse()
            response.message(menu_message)
            return HttpResponse(str(response))

        else:
            # If the user is not associated with any companies, handle accordingly
            response = MessagingResponse()
            response.message("You are not associated with any companies.")
            return HttpResponse(str(response))

    except WhatsAppNumber.DoesNotExist:
        # Handle the case when the WhatsApp number is not found in the database
        response = MessagingResponse()
        response.message("Your WhatsApp number is not registered.")
        return HttpResponse(str(response))



def send_whatsapp_message(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_='whatsapp:' + settings.TWILIO_PHONE_NUMBER,
        to='whatsapp:' + to
    )

    return message.sid
