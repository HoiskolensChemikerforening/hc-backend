from .models import RefoundRequest, Refound
from django.contrib import admin


@admin.register(RefoundRequest)
class RefoundAdmin(admin.ModelAdmin):
    ordering = ("created",)
    list_display = ("total_sum","user", "created", "number_of_receipts",)

    def number_of_receipts(self, obj):
        return obj.get_amount_receipts()

    def total_sum(self, obj):
        return f"Søknad om {obj.get_total()} kr"


@admin.register(Refound)
class RefoundAdmin(admin.ModelAdmin):
    ordering = ("date",)
    list_display = ("date", "store", "event", "price")
