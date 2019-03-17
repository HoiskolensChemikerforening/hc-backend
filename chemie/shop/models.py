from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
import datetime
from collections import deque

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

    def __str__(self):
        return f"Påfyllingskvittering {self.id}"


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Kategori", unique=True
    )
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=40, verbose_name="Varenavn", unique=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Pris"
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Varebeskrivelse",
        blank=True,
        null=True,
        default=None,
    )
    category = models.ForeignKey(
        Category, verbose_name="Kategori", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="shopitems", verbose_name="Bilde")

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if self.price < 0:
            raise ValidationError(
                "Du kan ikke legge inn en vare som gjør at vi taper penger. Wtf?"
            )
        super().clean(*args, **kwargs)


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item, verbose_name="Varenavn", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name="Antall")
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.item.name

    @classmethod
    def get_admin_list(cls):
        admin_list = deque(maxlen=12)
        all_items = Item.objects.all()
        for i in range(12):
            admin_list.append({})
            for item in all_items:
                admin_list[i][item.name] = 0

        order_items = cls.objects.all().order_by('-date')
        for item in order_items:
            purchase_month = int(item.date.month)
            item_name = str(item.item.name)
            if item_name in admin_list[purchase_month]:
                admin_list[purchase_month][item_name] += item.quantity
        this_month = int(datetime.datetime.now().month)
        admin_list.rotate(-(this_month+1))

        reversed_admin_list=[]
        for i in range(12,0,-1):
            reversed_admin_list.append(admin_list[i-1])
        return reversed_admin_list


class Order(models.Model):
    items = models.ManyToManyField(OrderItem, related_name="order")
    buyer = models.ForeignKey(
        User,
        verbose_name="Kjøper",
        related_name="orders",
        on_delete=models.CASCADE,
    )

    def get_total_price(self):
        totalprice = 0
        for item in self.items.all():
            totalprice += item.item.price * item.quantity
        return totalprice

    def __str__(self):
        return self.buyer.get_full_name() + " ordre " + str(self.id)


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

    def set(self, product, quantity=1):
        # Used for
        item = product.name
        if item not in self.cart:
            # Necessary conversion to comma for items to use same decimal separator
            price = str(product.price).replace(".", ",")
            self.cart[item] = {"quantity": 0, "price": price}
        self.cart[item]["quantity"] = quantity
        self.save()

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

    def buy(self, request):
        user = request.user
        order_items = []
        for item in self.cart.keys():
            item_object = get_object_or_404(Item, name=item)
            order_items.append(
                OrderItem.objects.create(
                    item=item_object, quantity=self.cart[item]["quantity"]
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
