from __future__ import unicode_literals
import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from .utils import update_glance


@python_2_unicode_compatible
class Integration(models.Model):

    SCOPE_SEND_NOTIFICATIONS = 'send_notification'

    SCOPES = [(SCOPE_SEND_NOTIFICATIONS, SCOPE_SEND_NOTIFICATIONS)]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    key = models.CharField(max_length=50, blank=True, null=True)
    homepage_url = models.URLField()
    url = models.URLField()
    scopes = models.CharField(max_length=50, choices=SCOPES)

    room_installable = models.BooleanField(default=True)
    globally_installable = models.BooleanField(default=False)

    @property
    def capabilities_url(self):
        return '{}/capabilities'.format(self.get_url())

    @property
    def installed_url(self):
        return '{}/installed'.format(self.get_url())

    def get_key(self):
        return self.key or self.id

    def get_url(self):
        return '{}/{}'.format(self.url, str(self.id))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class WebPanel(models.Model):
    TYPE_SIDEBAR = 'sidebar'

    TYPES = [(TYPE_SIDEBAR, TYPE_SIDEBAR)]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    integration = models.ForeignKey(Integration, related_name='panels')
    panel_type = models.CharField(max_length=50, choices=TYPES)
    key = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    location = models.CharField(max_length=255,
                                default='hipchat.sidebar.right')
    icon_url = models.URLField(blank=True, null=True)
    icon_url_2x = models.URLField(blank=True, null=True)

    def get_key(self):
        return self.key or self.id

    def get_url(self):
        return '{}/{}/{}'.format(self.integration.get_url(),
                                 self.panel_type,
                                 str(self.id))

    def __str__(self):
        return "{} @ {}".format(self.name, self.integration)


@python_2_unicode_compatible
class Glance(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    integration = models.ForeignKey(Integration, related_name='glances')
    key = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    target = models.CharField(max_length=255, blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    icon_url_2x = models.URLField(blank=True, null=True)

    def get_key(self):
        return self.key or self.id

    def get_url(self):
        return '{}/glance/{}'.format(self.integration.get_url(), str(self.id))

    def update_label(self, installation, new_label):
        """
        Updates glance label.
        """
        return update_glance(
            installation=installation,
            glace=self,
            new_label=new_label
        )

    def __str__(self):
        return "{} @ {}".format(self.name, self.integration)


@python_2_unicode_compatible
class Webhook(models.Model):

    EVENT_ROOM_MESSAGE = 'room_message'
    EVENTS = [(EVENT_ROOM_MESSAGE, EVENT_ROOM_MESSAGE)]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    integration = models.ForeignKey(Integration, related_name='webhooks')
    event = models.CharField(max_length=50, choices=EVENTS)
    name = models.CharField(max_length=255)
    url = models.URLField()
    pattern = models.CharField(max_length=255, blank=True, null=True)

    def get_key(self):
        return self.key or self.id

    def get_url(self):
        return '{}/webhook/{}'.format(self.integration.get_url(), str(self.id))

    def __str__(self):
        return "{} for {} @ {}".format(self.name, self.event, self.integration)


@python_2_unicode_compatible
class Installation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    integration = models.ForeignKey(Integration,
                                    related_name='installations',
                                    blank=True,
                                    null=True)
    capabilities_url = models.URLField()
    room_id = models.IntegerField()
    group_id = models.IntegerField()
    oauth_id = models.UUIDField()
    oauth_secret = models.CharField(max_length=255)
    uninstalled = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.room_id)
