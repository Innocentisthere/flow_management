from django.contrib import admin

# Register your models here.

from .models import MoneyFlow, Type, Category, Subcategory, MoneyFlow, Status

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(MoneyFlow)