from django.contrib import admin

from .models import Committee, Position
from chemie.events.admin import DropdownFilter


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    ordering = ('title',)
    search_fields = ('title',)
    list_display = ('title', 'email',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_filter = ('can_manage_committee', ('committee', DropdownFilter),)
    ordering = ('-committee',)
    search_fields = ('users__username', 'users__first_name', 'users__last_name',
                     'title',)
    list_display = ('title', 'committee', 'email', 'can_manage_committee',)
