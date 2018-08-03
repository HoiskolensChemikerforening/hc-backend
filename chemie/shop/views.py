from django.shortcuts import render
from .models import Item, ShoppingCart
from django.shortcuts import get_object_or_404


def index(request):
    items = Item.objects.all()
    cart = ShoppingCart(request)
    context = { 'items': items, 'cart': cart }
    if request.method == 'POST':
        if 'buy' in request.POST:
            item_id = request.POST['buy']
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item)
    return render(request, 'shop/shop.html', context)
