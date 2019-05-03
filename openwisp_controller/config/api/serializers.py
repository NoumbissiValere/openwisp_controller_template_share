from openwisp_utils.api.serializers import ValidatedModelSerializer
from ...config.models import Template


class TemplateRetrieveSerializer(ValidatedModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'type', 'variable', 'key', 'auto_cert',
                  'backend', 'vpn', 'url', 'config')


class TemplateSearchSerializer(ValidatedModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'description', 'organization')
