from django.contrib import admin

from apps.commission.models import Commission


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    pass
