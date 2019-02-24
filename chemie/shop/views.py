from django.shortcuts import render, redirect, reverse
from .models import Item, ShoppingCart
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RefillBalanceForm, AddCategoryForm, AddItemForm


@login_required
def index(request):
    items = Item.objects.all()
    cart = ShoppingCart(request)
    context = {"items": items, "cart": cart}
    if request.method == "POST":
        if "buy" in request.POST:
            item_id = request.POST["buy"]
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item)
        if "checkout" in request.POST:
            balance = request.user.profile.balance
            total_price = cart.get_total_price()
            if balance < total_price:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Du har itj pæng, kiis",
                    extra_tags="Nei!",
                )
            else:
                cart.buy(request)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Kontoen din er trukket {}".format(total_price),
                    extra_tags="Kjøp godkjent",
                )
                context["cart"] = cart
    return render(request, "shop/shop.html", context)


@permission_required("shop.can_refill_balance")
def refill(request):
    # provider = request.user.profile
    form = RefillBalanceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user_to_refill = form.cleaned_data.get("user")
            amount = form.cleaned_data.get("amount")
            user_to_refill.profile.balance += amount
            user_to_refill.profile.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Du har fylt på {} kr til brukeren {}".format(
                    amount, user_to_refill.username
                ),
                extra_tags="Suksess",
            )
    return render(request, "shop/refill-balance.html", {"form": form})


def add_item(request):
    form = AddItemForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:index"))
    context = {"form": form}
    return render(request, "shop/add_item.html", context)


def add_category(request):
    form = AddCategoryForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:index"))
    context = {"form": form}
    return render(request, "shop/add_category.html", context)
