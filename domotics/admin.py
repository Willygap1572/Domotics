from django.contrib import admin
from .models import Sensor, Switch, Clock, Rule, Activator


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('aid', 'name', 'theme', 'broker_host', 'port', 'state', 'fail')


class SensorAdmin(admin.ModelAdmin):
    list_display = ('aid', 'name', 'theme', 'broker_host', 'port', 'state', 'min', 'max', 'interval', 'increment')


class ClockAdmin(admin.ModelAdmin):
    list_display = ('aid', 'name', 'theme', 'broker_host', 'port', 'state', 'time', 'increment', 'rate')


class RuleAdmin(admin.ModelAdmin):
    list_display = ('activator', 'switch', 'threshold', 'type')


class ActivatorAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Activator, ActivatorAdmin)
admin.site.register(Switch, SwitchAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Clock, ClockAdmin)
admin.site.register(Rule, RuleAdmin)
