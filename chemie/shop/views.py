from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, reverse

from .forms import RefillBalanceForm, AddCategoryForm, AddItemForm
from .models import Item, ShoppingCart


@login_required
def index(request):
    items = Item.objects.all()
    cart = ShoppingCart(request)
    context = {"items": items, "cart": cart}
    if request.method == "POST":
        if "buy" in request.POST:
            post_str = request.POST["buy"]
            item_id, quantity = post_str.split("-")
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item, quantity=int(quantity))
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


@permission_required("customprofile.refill_balance")
def refill(request):
    provider = request.user
    form = RefillBalanceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            receiver = form.cleaned_data.get("receiver")
            amount = form.cleaned_data.get("amount")
            receiver.profile.balance += amount
            receiver.profile.save()
            instance = form.save(commit=False)
            instance.provider = provider
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Du har fylt på {} kr til brukeren {}".format(
                    amount, receiver.username
                ),
                extra_tags="Suksess",
            )
    return render(request, "shop/refill-balance.html", {"form": form})


@permission_required("shop.add_item")
def add_item(request):
    form = AddItemForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:index"))
    context = {"form": form}
    return render(request, "shop/add_item.html", context)


@permission_required("shop.add_category")
def add_category(request):
    form = AddCategoryForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:index"))
    context = {"form": form}
    return render(request, "shop/add_category.html", context)
