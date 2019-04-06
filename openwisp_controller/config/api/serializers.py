from openwisp_utils.api.serializers import ValidatedModelSerializer
from ...config.models import Template

class TemplateRetrieveSerializer(ValidatedModelSerializer):
    class Meta:
        model = Template
        fields = ('name', 'organization', 'backend', 'config',
                  'type')

