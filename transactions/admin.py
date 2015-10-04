from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import (
    TabularDynamicInlineAdmin)
from mezzanine.pages.admin import PageAdmin
from .models import Accounts, Items, Transactions

#admin.site.register(Accounts, PageAdmin)
#admin.site.register(Items, PageAdmin)

admin.site.register(Items, PageAdmin)

# Register your models here.
