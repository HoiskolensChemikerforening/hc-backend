from django.contrib import admin
from django.contrib.admin.filters import ChoicesFieldListFilter
from django.contrib.auth.admin import UserAdmin as BuiltinUserAdmin
from django.contrib.auth.forms import UserChangeForm as OldUserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class UserCreateForm(OldUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class DropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class UserInline(admin.StackedInline):
    model = Profile


class UserAdmin(BuiltinUserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    form = UserCreateForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', ('profile__grade', DropdownFilter),
                   ('profile__start_year', DropdownFilter), ('profile__end_year', DropdownFilter),
                   'profile__relationship_status')
    inlines = [UserInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
