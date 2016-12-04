from django.contrib import admin

from .models import (
    Integration,
    WebPanel,
    Glance,
    Webhook,
    Installation
)


admin.site.register(Integration)
admin.site.register(WebPanel)
admin.site.register(Glance)
admin.site.register(Webhook)
admin.site.register(Installation)
