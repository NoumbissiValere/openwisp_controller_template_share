from .generics import BaseGetTemplateView
from ...config.models import Template


class SharedTemplate(BaseGetTemplateView):
    template_model = Template
    queryset = Template.objects.none()


import_template = SharedTemplate.as_view()