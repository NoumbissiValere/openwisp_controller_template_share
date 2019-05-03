from .generics import BaseGetTemplateView
from django_netjsonconfig.api.generics import BaseSearchTemplate
from .serializers import TemplateSearchSerializer
from rest_framework.response import Response
from ...config.models import Template


class SharedTemplate(BaseGetTemplateView):
    template_model = Template
    queryset = Template.objects.none()


class SearchTemplate(BaseSearchTemplate):
    serializer_class = TemplateSearchSerializer
    template_model = Template

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        org = self.kwargs.get('org')
        if org:
            data = data.filter(organization=org)
        serializer = TemplateSearchSerializer(data, many=True)
        return Response(serializer.data)


search_template = SearchTemplate.as_view()
share_template = SharedTemplate.as_view()
