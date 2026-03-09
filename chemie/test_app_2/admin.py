from django.contrib import admin
from .models import Member, Role, Scheme, Investment


admin.site.register(Role)
admin.site.register(Scheme)
admin.site.register(Member)
admin.site.register(Investment)