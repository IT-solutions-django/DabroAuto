from django.contrib import admin

from django.contrib import admin
from .models import *


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryBody)
class DeliveryBodyAdmin(admin.ModelAdmin):
    pass
