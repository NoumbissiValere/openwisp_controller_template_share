from openwisp_utils.api.serializers import ValidatedModelSerializer
from ...config.models import Template

class TemplateRetrieveSerializer(ValidatedModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'type', 'variable', 'key', 'flag',
                  'auto_cert', 'backend', 'vpn', 'url', 'name', 'config')


