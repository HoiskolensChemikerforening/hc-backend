from django.shortcuts import render
from .models import Item, ShoppingCart
from django.shortcuts import get_object_or_404
from django.contrib import messages


def index(request):
    items = Item.objects.all()
    cart = ShoppingCart(request)
    context = { 'items': items, 'cart': cart }
    if request.method == 'POST':
        if 'buy' in request.POST:
            item_id = request.POST['buy']
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item)
        if 'checkout' in request.POST:
            balance = request.user.profile.balance
            total_price = cart.get_total_price()
            if balance < total_price:
                messages.add_message(request, messages.ERROR, 'Du har itj pæng, kiis', extra_tags='Nei!')
            else:
                cart.buy(request)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Kontoen din er trukket {}'.format(total_price),
                    extra_tags='Kjøp godkjent'
                )
                context['cart'] = cart
    return render(request, 'shop/shop.html', context)
