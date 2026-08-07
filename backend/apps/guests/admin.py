from django.contrib import admin

from .models import DiscountCategory, Guest

admin.site.register(Guest)
admin.site.register(DiscountCategory)
