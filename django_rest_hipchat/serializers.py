from rest_framework import serializers


class CapabilitiesSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return {
            'name': obj.name,
            'description': obj.description,
            'key': obj.get_key(),
            'links': {
                'homepage': obj.homepage_url,
                'self': obj.capabilities_url
            },
            'capabilities': {
                'hipchatApiConsumer': {
                    'scopes': obj.scopes.split(',')
                },
                'webPanel': [
                    WebPanelSerializer(instance=panel).data
                    for panel in obj.panels.all()
                ],
                'glance': [
                    GlanceSerializer(instance=glance).data
                    for glance in obj.glances.all()
                ],
                'webhook': [
                    WebhookSerializer(instance=webhook).data
                    for webhook in obj.webhooks.all()
                ],
                'installable': {
                    'allowGlobal': obj.globally_installable,
                    'allowRoom': obj.room_installable,
                    'callbackUrl': obj.installed_url
                },
            }
        }


class WebPanelSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        data = {
            'key': obj.get_key(),
            'name': {'value': obj.name},
            'url': obj.get_url(),
            'location': obj.location
        }
        if obj.icon_url:
            data['icon'] = {
                'url': obj.icon_url,
                'url@2x': obj.icon_url_2x or obj.icon_url
            }
        return data


class GlanceSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        data = {
            'name': {'value': obj.name},
            'queryUrl': obj.get_url(),
            'key': obj.get_key(),
            'icon': {
                'url': obj.icon_url,
                'url@2x': obj.icon_url_2x or obj.icon_url
            },
            'conditions': []
        }

        if obj.target:
            data['target'] = obj.target
        return data


class WebhookSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'event': obj.event,
            'pattern': obj.pattern,
            'url': obj.get_url(),
            'name': obj.name,
            'authentication': 'jwt'
        }
