from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from extended_choices import Choices
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


HAPPY_HOUR_DURATION = Choices(
    ("ONE", 1, "1 time"),
    ("TWO", 2, "2 timer"),
    ("THREE", 3, "3 timer"),
    ("FOUR", 4, "4 timer"),
    ("FIVE", 5, "5 timer"),
)


class RefillReceipt(models.Model):
    # Is responsible for refilling balance
    provider = models.ForeignKey(
        User, verbose_name="Regnskapsfører", on_delete=models.CASCADE
    )
    # Person who gets money on their account
    receiver = models.ForeignKey(
        User,
        related_name="refill",
        verbose_name="Mottaker",
        on_delete=models.CASCADE,
    )
    # Amount of money received
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="HC-coin"
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Påfyllingskvittering {self.id}"


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Kategori", unique=True
    )
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def check_active_without_tablet_category(self):
        count = self.item.filter(
            is_active=True, buy_without_tablet=True
        ).count()
        if count > 0:
            return True
        else:
            return False

    def check_active_category(self):
        count = self.item.filter(is_active=True).count()
        if count > 0:
            return True
        else:
            return False


class Item(models.Model):
    name = models.CharField(
        max_length=40, verbose_name="Varenavn", unique=True
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Pris"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Kategori",
        on_delete=models.CASCADE,
        related_name="item",
    )
    image = models.ImageField(upload_to="shopitems", verbose_name="Bilde")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    happy_hour_duplicate = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        verbose_name="Happy Hour duplikat",
        on_delete=models.DO_NOTHING,
    )

    buy_without_tablet = models.BooleanField(
        default=False, verbose_name="Kunde kan kjøpe vare med telefon?"
    )

    @classmethod
    def get_active_items(cls):
        active_items = cls.objects.filter(
            is_active=True, buy_without_tablet=True
        )
        return active_items

    @classmethod
    def get_active_tablet_items(cls):
        active_items = cls.objects.filter(is_active=True)
        return active_items

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if self.price is not None:
            if self.price < 0:
                raise ValidationError(
                    "Du kan ikke legge inn en vare som gjør at vi taper penger. Wtf?"
                )
        super().clean(*args, **kwargs)


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item, verbose_name="Varenavn", on_delete=models.DO_NOTHING
    )
    quantity = models.PositiveIntegerField(verbose_name="Antall")

    total_price = models.PositiveIntegerField(
        verbose_name="Totalpris", default=0
    )

    def __str__(self):
        return self.item.name


class Order(models.Model):
    items = models.ManyToManyField(OrderItem, related_name="order")
    buyer = models.ForeignKey(
        User,
        verbose_name="Kjøper",
        related_name="orders",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.buyer.get_full_name() + " ordre " + str(self.id)

    def get_total_price(self):
        totalprice = 0
        for item in self.items.all():
            totalprice += item.total_price
        return totalprice

    def __lt__(self):
        pass


class HappyHour(models.Model):
    provider = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Oprettet")
    duration = models.PositiveSmallIntegerField(
        choices=HAPPY_HOUR_DURATION,
        verbose_name="Varighet",
        default=HAPPY_HOUR_DURATION.ONE,
    )

    def __str__(self):
        return f"Happy Hour {self.id} av {self.provider.get_full_name()}"

    def send_push(self, subscribers):
        for subscriber in subscribers:
            devices = subscriber.profile.devices.all()
            tag = (
                "1 time"
                if self.duration == 1
                else "{} timer".format(self.duration)
            )
            happyhour_message = "Nå er det Happy Hour i {} på kontoret".format(
                tag
            )
            for device in devices:
                device.send_notification("Happy Hour!", happyhour_message)


class ShoppingCart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        # Method can be used to create items in the Shopcart if it does not already exist
        # and update quantity of item
        item = product.name
        if item not in self.cart:
            price = str(product.price).replace(".", ",")
            self.cart[item] = {"quantity": 0, "price": price}
        if self.cart[item]["quantity"] + quantity >= 0:
            self.cart[item]["quantity"] += quantity
            self.save()

    def subtract(self, product, quantity=1):
        if quantity > 0:
            self.add(product, -quantity)

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        item = product.name
        if item in self.cart:
            del self.cart[item]
            self.save()

    def __iter__(self):
        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def get_total_price(self):
        # Decimal conversion may only be performed if string has dot as decimal separator
        return sum(
            Decimal(item["price"].replace(",", ".")) * item["quantity"]
            for item in self.cart.values()
        )

    def buy(self, user):
        order_items = []
        for item in self.cart.keys():
            item_object = get_object_or_404(Item, name=item)
            order_items.append(
                OrderItem.objects.create(
                    item=item_object,
                    quantity=self.cart[item]["quantity"],
                    total_price=self.cart[item]["quantity"]
                    * item_object.price,
                )
            )
        order = Order.objects.create(buyer=user)
        order.items.add(*order_items)
        order.save()
        user.profile.balance -= self.get_total_price()
        user.profile.save()
        self.clear()

    def clear(self):
        self.cart = {}
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    instance.slug = slug


pre_save.connect(pre_save_category_receiver, sender=Category)
