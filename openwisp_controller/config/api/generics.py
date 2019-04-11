import json
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, get_object_or_404,
)
from rest_framework.response import Response
from openwisp_users.models import Organization
from .serializers import TemplateRetrieveSerializer


class BaseGetTemplateView(RetrieveAPIView):
    serializer_class = TemplateRetrieveSerializer

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key', None)
        if key is None:
            temp = get_object_or_404(self.template_model, pk=kwargs['uuid'], flag='public')
        else:
            temp = get_object_or_404(self.template_model, pk=kwargs['uuid'], key=key,
                                     flag='shared_secret')
        serializer = TemplateRetrieveSerializer(temp)
        return Response(serializer.data)


