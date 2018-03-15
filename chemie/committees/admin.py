from django.contrib import admin

from .models import Committee, Position
from chemie.events.admin import DropdownFilter
from django.contrib.auth.models import User


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    ordering = ('title',)
    search_fields = ('title',)
    list_display = ('title', 'email',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_filter = ('can_manage_committee', ('committee', DropdownFilter),)
    ordering = ('-committee',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'title',)
    list_display = ('title', 'committee', 'email', 'can_manage_committee',)


#admin.site.register(Committee)
#admin.site.register(Position)
