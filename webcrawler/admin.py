from django.contrib import admin
from .models import ValuationRoll, RollQue
# Register your models here.


class ValuationRollAdmin(admin.ModelAdmin):
    list_display = ('rate_number', 'roll_type', 'legal_description', 'use_code', 'market_value', 'suburb', 'deeds_town', 'scheme')


class RollQueAdmin(admin.ModelAdmin):
    list_display = ('deeds_town', 'suburb', 'scheme')

admin.site.register(ValuationRoll, ValuationRollAdmin)
admin.site.register(RollQue, RollQueAdmin)
