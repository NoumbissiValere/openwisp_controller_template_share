from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, get_object_or_404,
)
from rest_framework.response import Response
from .serializers import TemplateRetrieveSerializer


class BaseGetTemplateView(RetrieveAPIView):
    serializer_class = TemplateRetrieveSerializer

    def get(self, request, *args, **kwargs):
        temp = get_object_or_404(self.template_model, pk=kwargs['uuid'])
        serializer = TemplateRetrieveSerializer(temp)
        return Response(serializer.data)

