from decimal import InvalidOperation

from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils import timezone
from django.utils.html import format_html
import operator


from chemie.customprofile.forms import GetRFIDForm
from chemie.web_push.models import Subscription
from chemie.customprofile.models import Profile
from .forms import (
    RefillBalanceForm,
    AddCategoryForm,
    AddItemForm,
    HappyHourForm,
    EditItemForm,
    GetUserRefillForm,
    GetUserReceiptsForm,
    SearchItemForm,
)
from .models import (
    Item,
    ShoppingCart,
    Category,
    Order,
    HappyHour,
    RefillReceipt,
)
from .statistics import get_plot_item


def is_happy_hour():
    now = timezone.now()
    try:
        latest_happy_hour = HappyHour.objects.latest("id")
        diff = now - latest_happy_hour.created
        time_active_seconds = diff.total_seconds()
        time_active_minutes = time_active_seconds / 60
        time_active_hours = time_active_minutes / 60
        if time_active_hours < latest_happy_hour.duration:
            is_happy = True
            time_left_hours = (
                float(latest_happy_hour.duration) - time_active_hours
            )
            time_left_minutes = time_left_hours * 60
        else:
            is_happy = False
            time_left_minutes = None
        return is_happy, time_left_minutes
    except HappyHour.DoesNotExist:
        return False, False


def get_last_year_receipts():
    all_receipts = Order.objects.all()
    now = timezone.now()
    # Get 11 months back
    if now.month == 12:
        first_date = timezone.datetime(year=now.year, month=1, day=1)
    else:
        first_date = timezone.datetime(
            year=now.year - 1, month=now.month + 1, day=1
        )
    receipts = all_receipts.filter(created__gte=first_date, created__lte=now)
    months, m, i = 12, 0, 0
    year, month = now.year, now.month
    item_quantity = []
    item_price = []
    monthTotal = []
    while i < months:
        # Get the receipts at current_month - m
        if (month - m) > 0:
            month_c = month - m
        else:
            year = now.year - 1
            month, month_c = 12, 12
            m = 0
        current_receipts = receipts.filter(
            created__year=year, created__month=month_c
        )
        monthTotal.append(0)
        item_quantity.append({})
        item_price.append({})
        for r in current_receipts:
            for order_item in r.items.all():
                order_item_key = order_item.item.name
                if order_item_key not in item_quantity[i]:
                    item_quantity[i][order_item_key] = order_item.quantity
                    item_price[i][order_item_key] = order_item.total_price
                    monthTotal[i] += order_item.total_price

                else:
                    item_quantity[i][order_item_key] += order_item.quantity
                    item_price[i][order_item_key] += order_item.total_price
                    monthTotal[i] += order_item.total_price

        if len(item_quantity[i]) > 0:
            sorted_item_quantity = sorted(
                item_quantity[i].items(),
                key=operator.itemgetter(1),
                reverse=True,
            )
            item_quantity[i] = dict(sorted_item_quantity)
        if len(item_price[i]) > 0:
            sorted_item_price = sorted(
                item_price[i].items(), key=operator.itemgetter(1), reverse=True
            )
            item_price[i] = dict(sorted_item_price)
        m += 1
        i += 1
    return item_quantity, item_price, monthTotal


@login_required
def index(request):
    if request.user.username == "tabletshop":
        context = index_tabletshop(request)
    else:
        context = index_user(request)
    context["is_happy"] = is_happy_hour()[0]
    return render(request, "shop/shop.html", context)


def index_user(request):
    is_tablet_user = False
    rfid_form = None
    items = Item.get_active_items().order_by("name")
    try:
        happy_item_ids = items.filter(
            happy_hour_duplicate__isnull=False
        ).values_list("happy_hour_duplicate", flat=True)
        items = items.exclude(id__in=happy_item_ids)
    except Category.DoesNotExist:
        pass
    categories = Category.objects.all()
    cart = ShoppingCart(request)
    context = {
        "items": items,
        "categories": categories,
        "cart": cart,
        "is_tablet_user": is_tablet_user,
        "rfid_form": rfid_form,
    }
    if request.method == "POST":
        if "buy" in request.POST:
            post_str = request.POST["buy"]
            item_id, quantity = post_str.split("-")
            if int(quantity) <= 0:
                return context
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item, quantity=int(quantity))

        if "checkout" in request.POST:
            user = request.user
            balance = user.profile.balance
            total_price = cart.get_total_price()
            if balance < total_price:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Du har itj nok HC-coins, kiis",
                    extra_tags="Nei!",
                )
            else:
                cart.buy(user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Kontoen din er trukket {} HC-coins".format(total_price),
                    extra_tags="Kjøp godkjent",
                )
                context["cart"] = cart
    return context


def index_tabletshop(request):
    is_tablet_user = True
    rfid_form = GetRFIDForm(request.POST or None)
    items = Item.get_active_tablet_items().order_by("name")
    try:
        happy_item_ids = items.filter(
            happy_hour_duplicate__isnull=False
        ).values_list("happy_hour_duplicate", flat=True)
        items = items.exclude(id__in=happy_item_ids)
    except Category.DoesNotExist:
        pass
    categories = Category.objects.all()
    cart = ShoppingCart(request)
    context = {
        "items": items,
        "categories": categories,
        "cart": cart,
        "is_tablet_user": is_tablet_user,
        "rfid_form": rfid_form,
    }
    if request.method == "POST":
        if "buy" in request.POST:
            post_str = request.POST["buy"]
            item_id, quantity = post_str.split("-")
            if int(quantity) <= 0:
                return context
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item, quantity=int(quantity))

        if "checkout" in request.POST:
            if rfid_form.is_valid():
                rfid = rfid_form.cleaned_data["rfid"]
                try:
                    access_card = Profile.objects.rfid_to_em(rfid)
                    profile = Profile.objects.get(access_card=access_card)
                    balance = profile.balance
                    total_price = cart.get_total_price()
                    if balance < total_price:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            f"{request.user.get_full_name()} sin konto har itj nok HC-coins, kiis. Saldo på konto er {balance} HC-coins",
                            extra_tags="Avvist",
                        )
                    else:
                        cart.buy(profile.user)
                        new_balance = balance - total_price
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            (
                                f"{profile.user.get_full_name()} sin konto er trukket {total_price} HC-coins."
                                f"Ny saldo på konto er: {new_balance} HC-coins."
                            ),
                            extra_tags="Kjøp godkjent",
                        )
                    context["cart"] = cart
                except ObjectDoesNotExist:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "Studentkort er ikke registrert. Logg inn på https://hc.ntnu.no{} og legg inn ditt studentkorts EM-nummer".format(
                            reverse("profile:edit")
                        ),
                        extra_tags="Ups",
                    )
    rfid_form = GetRFIDForm(None)
    context["rfid_form"] = rfid_form
    return context


@login_required
def view_my_receipts(request):
    orders = (
        Order.objects.filter(buyer=request.user)
        .order_by("-created")
        .prefetch_related("items")
    )
    return render(request, "shop/user_receipts.html", {"orders": orders})


@login_required
def view_my_refills(request):
    refill_receipts = RefillReceipt.objects.filter(
        receiver=request.user
    ).order_by("-created")
    return render(
        request, "shop/user_refills.html", {"refill_receipts": refill_receipts}
    )


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Item.objects.none()

        qs = Item.objects.all().order_by("name")

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

    def get_result_label(self, item):
        return format_html("{}", item.name)


@login_required
def view_statistics(request):
    items = Item.objects.all()
    orders = (
        Order.objects.filter(buyer=request.user)
        .order_by("-created")
        .prefetch_related("items")
    )
    bought_items = request.user.profile.get_bought_items()
    search_form = SearchItemForm(request.POST or None)
    context = {
        "items": items,
        "orders": orders,
        "bought_items": bought_items,
        "search_form": search_form,
    }
    if request.method == "POST":
        if search_form.is_valid():
            plot_item_id = search_form.data["name"]
            plot_item, plot_time, plot_quantity = get_plot_item(
                request.user, plot_item_id
            )
            context["plot_time"] = plot_time
            context["plot_quantity"] = plot_quantity
            context["plot_item"] = plot_item
            context["seatch_form"] = SearchItemForm(None)
            context["item_name"] = plot_item.name
    return render(request, "shop/user_statistics.html", context)


@permission_required("customprofile.refill_balance")
def admin(request):
    return render(request, "shop/admin.html")


@permission_required("customprofile.refill_balance")
def refill(request):
    provider = request.user
    form = RefillBalanceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            receiver = form.cleaned_data.get("receiver")
            if receiver == request.user:
                messages.add_message(
                    request,
                    messages.ERROR,
                    (
                        "Du kan ikke fylle på HC-coins til deg selv. "
                        "Påfyller kan ikke være den samme som mottaker."
                    ),
                    extra_tags="Feil",
                )
            else:
                amount = form.cleaned_data.get("amount")
                try:
                    receiver.profile.balance += amount
                    receiver.profile.save()
                except InvalidOperation:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        (
                            "Brukeren vil få mer enn 9999 HC-coins på "
                            "konto om du fyller på med beløpet."
                        ),
                        extra_tags="Feil",
                    )
                    return render(
                        request, "shop/refill-balance.html", {"form": form}
                    )
                instance = form.save(commit=False)
                instance.provider = provider
                instance.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Du har fylt på {} HC-coins til {}".format(
                        amount, receiver.get_full_name()
                    ),
                    extra_tags="Suksess",
                )
            return redirect("shop:refill")
    return render(request, "shop/refill-balance.html", {"form": form})


@permission_required("shop.add_item")
def add_item(request):
    form = AddItemForm(None, None)
    items = Item.objects.filter(is_active=True).order_by("name")
    initial_checkbox_state = True

    if request.POST:
        if ("checkForm" in request.POST.keys()) and ("filterActiveItems" in request.POST.keys()): #IsActive form er checked
            items = Item.objects.filter(is_active=True).order_by("name")

        elif "checkForm" in request.POST.keys(): #IsActive form unchecked
            items = Item.objects.order_by("name")
            initial_checkbox_state = False

        else: #Add item form posted
            form = AddItemForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Varen ble opprettet",
                    extra_tags="Suksess!",
                )
                form.save()
                form = AddItemForm(None, None)

    context = {"form": form, "items": items, "initialCheckboxState": initial_checkbox_state}

    return render(request, "shop/add_item.html", context)


@permission_required("shop.change_item")
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = EditItemForm(
        request.POST or None, request.FILES or None, instance=item
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Varen ble endret.",
                extra_tags="Endret!",
            )
            return redirect(reverse("shop:add-item"))
    context = {"form": form}
    return render(request, "shop/edit_item.html", context)


@permission_required("shop.add_category")
def add_category(request):
    form = AddCategoryForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
    categories = Category.objects.all()
    context = {"form": form, "categories": categories}
    return render(request, "shop/add_category.html", context)


@login_required
def remove_item(request, pk):
    item = Item.objects.get(pk=pk)
    cart = ShoppingCart(request)
    cart.remove(item)
    return JsonResponse({"success": 1})


@login_required
def remove_cart(request):
    cart = ShoppingCart(request)
    cart.clear()
    return JsonResponse({"success": 1})


@permission_required("shop.add_happyhour")
def activate_happyhour(request):
    form = HappyHourForm(request.POST or None)
    try:
        is_happy, time_left_minutes = is_happy_hour()
        if is_happy:
            messages.add_message(
                request,
                messages.WARNING,
                f"Happy Hour er allerede aktivert. Det er {round(time_left_minutes)} minutter igjen",
            )
            return redirect(reverse("shop:admin"))
        return create_happyhour(request, form)
    except HappyHour.DoesNotExist:
        print("Ingen Happy Hour-objekter eksisterer")
        return create_happyhour(request, form)
    except:
        messages.add_message(
            request,
            messages.WARNING,
            "Vi har en teknisk feil og vil prøve å rette opp i det",
            extra_tags="Vennligst ta kontakt med Webkom",
        )
        context = {"form": form}
        return render(request, "shop/happy-hour.html", context)


@permission_required("shop.add_happyhour")
def create_happyhour(request, form):
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.provider = user
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Happy Hour aktivert!",
                extra_tags=f"Aktivert i {instance.duration} time(r)",
            )
            subscriptions = Subscription.objects.filter(subscription_type=3)
            subscribers = [sub.owner for sub in subscriptions]
            instance.send_push(subscribers)
            return redirect(reverse("shop:admin"))
    context = {"form": form}
    return render(request, "shop/happy-hour.html", context)


@permission_required("customprofile.refill_balance")
def view_all_receipts(request):
    form = GetUserReceiptsForm(request.POST or None)
    context = {"form": form}
    try:
        if request.method == "POST":
            if form.is_valid():
                user = form.cleaned_data.get("buyer")
                orders = (
                    Order.objects.filter(buyer=user)
                    .order_by("-created")
                    .prefetch_related("items")
                )
                context["orders"] = orders
                context["buyer"] = user
        else:
            orders = Order.objects.order_by("-created")[:100]
            context["orders"] = orders
    except ObjectDoesNotExist:
        pass

    return render(request, "shop/all_receipts.html", context)


@permission_required("customprofile.refill_balance")
def view_all_refills(request):
    form = GetUserRefillForm(request.POST or None)
    context = {"form": form}
    try:
        if request.method == "POST":
            if form.is_valid():
                receiver = form.cleaned_data.get("receiver")
                refill_receipts = RefillReceipt.objects.order_by("-created")[:100]
                context["refill_receipts"] = refill_receipts
                context["receiver"] = receiver
        else:
            refill_receipts = RefillReceipt.objects.all().order_by("-created")[:100]
            context["refill_receipts"] = refill_receipts
    except ObjectDoesNotExist:
        pass
    refill_sum_active = Profile.get_balance_sum_for_first_to_fifth_grades()
    context["refill_sum_active"] = refill_sum_active
    refill_sum_total = Profile.get_all_refill_sum()
    context["refill_sum_total"] = refill_sum_total
    return render(request, "shop/all_refills.html", context)


@permission_required("customprofile.refill_balance")
def view_monthly_statistics(request):
    order_items, order_price, monthTotal = get_last_year_receipts()
    items = Item.objects.all()
    return render(
        request,
        "shop/monthly_statistics.html",
        {
            "monthTotal": monthTotal,
            "order_items": order_items,
            "order_price": order_price,
            "items": items,
        },
    )
