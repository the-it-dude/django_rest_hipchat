from django.contrib import admin

from .models import (
    Integration,
    WebPanel,
    Glance,
    Webhook,
    Installation
)


class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'capabilities_url')


class InstallationAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'group_id', 'integration', 'uninstalled')


admin.site.register(Integration, IntegrationAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(WebPanel)
admin.site.register(Glance)
admin.site.register(Webhook)
