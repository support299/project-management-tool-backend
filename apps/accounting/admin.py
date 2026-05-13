from django.contrib import admin

from .models import Expense, Invoice

admin.site.register(Invoice)
admin.site.register(Expense)
