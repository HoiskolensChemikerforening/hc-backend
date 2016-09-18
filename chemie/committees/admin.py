from django.contrib import admin

from .models import Committee, Member, Position

admin.site.register(Committee)
admin.site.register(Member)
admin.site.register(Position)
