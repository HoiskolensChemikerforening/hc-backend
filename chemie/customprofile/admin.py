from django.contrib import admin
from django.contrib.admin.filters import ChoicesFieldListFilter
from django.contrib.auth.admin import UserAdmin as BuiltinUserAdmin
from django.contrib.auth.forms import UserChangeForm as OldUserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile, Medal


def export_csv(modeladmin, request, queryset):
    # Credits to https://djangotricks.blogspot.no/2013/12/how-to-export-data-as-excel.html
    import csv
    from django.utils.encoding import smart_str
    from django.http.response import HttpResponse

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=users.csv"
    writer = csv.writer(response, csv.excel)
    response.write(
        "\ufeff".encode("utf8")
    )  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(
        [
            smart_str("First name"),
            smart_str("Last name"),
            smart_str("Email"),
            smart_str("Grade"),
            smart_str("Username"),
        ]
    )
    for obj in queryset:
        try:
            grade = obj.profile.grade
        except ObjectDoesNotExist:
            grade = ""

        writer.writerow(
            [
                smart_str(obj.first_name),
                smart_str(obj.last_name),
                smart_str(obj.email),
                smart_str(grade),
                smart_str(obj.username),
            ]
        )
    return response


export_csv.short_description = "Export CSV"


class UserCreateForm(OldUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class DropdownFilter(ChoicesFieldListFilter):
    template = "admin/dropdown_filter.html"


class UserInline(admin.StackedInline):
    model = Profile
    readonly_fields = ("balance",)


class UserAdmin(BuiltinUserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    form = UserCreateForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        ("profile__grade", DropdownFilter),
        ("profile__start_year", DropdownFilter),
        ("profile__end_year", DropdownFilter),
        "profile__relationship_status",
        "profile__specialization",
        "profile__devices",
        "profile__subscriptions",
    )
    inlines = [UserInline]
    actions = [export_csv]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Medal)
