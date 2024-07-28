from home.models import contact_phone

def contact_context(request):
    contact_phone_number = contact_phone.objects.first()
    return {'contact_phone_number': contact_phone_number}

