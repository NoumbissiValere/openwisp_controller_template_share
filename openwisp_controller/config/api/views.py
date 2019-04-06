from .generics import BaseGetTemplateView
from ...config.models import Template

class PublicTemplate(BaseGetTemplateView):
    template_model = Template
    queryset = Template.objects.none()

import_template = PublicTemplate.as_view()