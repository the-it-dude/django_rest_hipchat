from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<integration_id>[0-9a-f\-]{36})/capabilities$',
        views.CabalitiesAPIView.as_view()),
    url(r'^(?P<integration_id>[0-9a-f\-]{36})/installed$',
        views.InstalledAPIView.as_view()),
    url(r'^(?P<integration_id>[0-9a-f\-]{36})/uninstalled$',
        views.UninstalledAPIView.as_view()),
    url(r'^(?P<integration_id>[0-9a-f\-]{36})/glance/(?P<glance_id>[0-9a-f\-]{36})$',
        views.GlanceAPIView.as_view()),
    url(r'^(?P<integration_id>[0-9a-f\-]{36})/sidebar/(?P<sidebar_id>[0-9a-f\-]{36})$',
        views.SidebarAPIView.as_view()),
    url(r'^(?P<integration_id>[0-9a-f\-]{36})/webhook/(?P<webhook_id>[0-9a-f\-]{36})$',
        views.WebhookAPIView.as_view()),
]
