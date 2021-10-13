from django.contrib import admin
from .models import (
    Social,
    SocialEventRegistration,
    RegistrationMessage,
    Bedpres,
    BedpresRegistration,
)
from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    RelatedFieldListFilter,
    ChoicesFieldListFilter,
)


def export_csv(modeladmin, request, queryset):
    # Credits to https://djangotricks.blogspot.no/2013/12/how-to-export-data-as-excel.html
    import csv
    from django.utils.encoding import smart_str
    from django.http.response import HttpResponse

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=registrations.csv"
    writer = csv.writer(response, csv.excel)
    response.write(
        u"\ufeff".encode("utf8")
    )  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(
        [
            smart_str(u"ID"),
            smart_str(u"Event"),
            smart_str(u"User"),
            smart_str(u"Created"),
            smart_str(u"Status"),
            smart_str(u"Payment Status"),
        ]
    )
    for obj in queryset:
        writer.writerow(
            [
                smart_str(obj.pk),
                smart_str(obj.event),
                smart_str(obj.user),
                smart_str(obj.created),
                smart_str(obj.status),
            ]
        )
    return response


export_csv.short_description = u"Export CSV"


class DropdownFilter(RelatedFieldListFilter):
    template = "admin/dropdown_filter.html"


@admin.register(SocialEventRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ("status", "payment_status", ("event", DropdownFilter))
    ordering = ("-created",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_display = (
        "event",
        "user",
        "created",
        "edited",
        "payment_status",
        "companion",
    )
    actions = [export_csv]


@admin.register(BedpresRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ("status", ("event", DropdownFilter))
    ordering = ("-created",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_display = ("event", "user", "created", "edited", "arrival_status")


@admin.register(Social)
class EventAdmin(admin.ModelAdmin):
    list_filter = ("date",)
    ordering = ("-date",)
    search_fields = ("title",)
    list_display = (
        "title",
        "sluts",
        "date",
        "created",
        "edited",
        "companion",
        "sleepover",
        "night_snack",
        "published",
    )


@admin.register(Bedpres)
class EventAdmin(admin.ModelAdmin):
    list_filter = ("date",)
    ordering = ("-date",)
    search_fields = ("title",)
    list_display = ("title", "sluts", "date", "created", "edited", "published")


# admin.site.register(RegistrationMessage)
