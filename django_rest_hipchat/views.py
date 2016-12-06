import logging
from django.views.generic import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from .forms import InstallationForm
from .models import Installation, Integration, WebPanel, Glance, Webhook
from .serializers import CapabilitiesSerializer

logger = logging.getLogger(__name__)


class IntegrationMixin(object):

    def get_integration(self, integration_id):
        try:
            return Integration.objects.get(
                id=integration_id
            )
        except Integration.DoesNotExist:
            return None


class CabalitiesAPIView(IntegrationMixin, APIView):

    def get(self, request, integration_id, format=None):
        logger.info("Capabilities request: {}".format(
            request.query_params))
        integration = self.get_integration(integration_id=integration_id)
        if integration is None:
            return Response(
                {'status': 'error', 'errors': ['Unknown registration']},
                status=HTTP_400_BAD_REQUEST
            )

        return Response(CapabilitiesSerializer(instance=integration).data)


class InstalledAPIView(IntegrationMixin, APIView):
    def post(self, request, integration_id, format=None):
        logger.warn("Installed request for {}: {}".format(
            self.get_integration(integration_id=integration_id),
            request.data
        ))

        form = InstallationForm(request.data)
        if form.is_valid():
            installation = Installation.objects.create(
                oauth_id=form.cleaned_data['oauthId'],
                oauth_secret=form.cleaned_data['oauthSecret'],
                capabilities_url=form.cleaned_data['capabilitiesUrl'],
                room_id=form.cleaned_data['roomId'],
                group_id=form.cleaned_data['groupId'],
            )
            return Response(
                {'status': 'ok', 'id': installation.id},
                status=HTTP_201_CREATED
            )
        return Response(
            {'status': 'error', 'errors': form.errors},
            status=HTTP_400_BAD_REQUEST
        )


class UninstalledAPIView(IntegrationMixin, APIView):
    def post(self, request, integration_id, format=None):
        logger.warn("Uninstaled request {}: {}".format(
            self.get_integration(integration_id=integration_id),
            request.data
        ))


class SidebarAPIView(IntegrationMixin, TemplateView):
    template_name = 'django_rest_hipchat/sidebar.html'

    def get_sidebar(self, integration):
        try:
            return integration.panels.get(
                id=self.kwargs['sidebar_id']
            )
        except WebPanel.DoesNotExist:
            return None

    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        logger.warn(repr(request.META))
        return super(SidebarAPIView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super(SidebarAPIView, self).get_context_data(*args, **kwargs)
        if self.request.GET.get('theme'):
            data['theme'] = self.request.GET['theme']

        data['sidebar'] = self.get_sidebar(
            self.get_integration(self.kwargs['integration_id'])
        )

        return data


class GlanceAPIView(IntegrationMixin, APIView):

    def get_glance(self, integration):
        try:
            return integration.glances.get(
                id=self.kwargs['glance_id']
            )
        except Glance.DoesNotExist:
            return None

    def get_data(self, glance):
        return {
            "label": {
                "type": "html",
                "value": "Sort of idle."
            },
        }

    def get(self, request, integration_id, glance_id, format=None):
        glance = self.get_glance(self.get_integration(integration_id))
        logger.warn("Glance request: {}".format(request.data))
        return Response(self.get_data(glance), status=HTTP_200_OK)


class WebhookAPIView(IntegrationMixin, APIView):
    def get_webhook(self, integration):
        try:
            return integration.webhooks.get(
                id=self.kwargs['webhook_id']
            )
        except Webhook.DoesNotExist:
            return None

    def post(self, request, integration_id, webhook_id, *args, **kwargs):
        webhook = self.get_webhook(self.get_integration(integration_id))

        response = self.process_webhook_message(webhook, request.data)
        if response is None:
            response = {'status': 'ok'}

        return Response(response, status=HTTP_200_OK)

    def process_webhook_message(self, webhook, message):
        logger.warn('Webhook message: {}'.format(repr(message)))
