from .models import RefoundRequest, Refound
from django.contrib import admin


@admin.register(RefoundRequest)
class RefoundAdmin(admin.ModelAdmin):
    """
    Class to display the RefoundRequest model on the admin page.
    """
    ordering = ("created",)
    list_display = ("total_sum", "user", "created", "number_of_receipts",)

    def number_of_receipts(self, obj):
        return obj.get_amount_receipts()

    def total_sum(self, obj):
        return f"Søknad om {obj.get_total()} kr"


@admin.register(Refound)
class RefoundAdmin(admin.ModelAdmin):
    """
    Class to display the Refound model on the admin page.
    """
    ordering = ("date",)
    list_display = ("receipt", "date", "store", "event", "price", "request_user", "request_sum", "request_date")

    def request_user(self, obj):
        return f"{obj.refoundrequest.user.first_name} {obj.refoundrequest.user.last_name}"

    def request_sum(self, obj):
        return f"{obj.refoundrequest.get_total()} kr"

    def request_date(self, obj):
        return f"{obj.refoundrequest.created.strftime('%d/%m/%Y')}"

    def receipt(self, obj):
        return f"Receipt ({obj.price} kr)"
