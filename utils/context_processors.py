from home.models import contact_phone


def contact_context(request):
    contact_phone_number = contact_phone.objects.first()
    return {'contact_phone_number': contact_phone_number, }


def sum_cart(request):
    sum_cart_value = request.session.get('cart', {})
    total_value = sum(item['quantity'] for item in sum_cart_value.values())
    return {'sum_cart': total_value, }

