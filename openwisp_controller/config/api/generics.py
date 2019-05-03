from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, get_object_or_404,
)
from rest_framework.response import Response
from .serializers import TemplateRetrieveSerializer, TemplateSearchSerializer
from ...config.models import Template


class BaseGetTemplateView(RetrieveAPIView):
    serializer_class = TemplateRetrieveSerializer

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key', None)
        if key:
            print(key, "the key \n\n\n\n\n\n\n")
            temp = get_object_or_404(self.template_model, pk=kwargs['uuid'], key=key,
                                     flag='shared_secret')
        else:
            temp = get_object_or_404(self.template_model, pk=kwargs['uuid'], flag='public')
        serializer = TemplateRetrieveSerializer(temp)
        return Response(serializer.data)


# class BaseSearchTemplate(ListAPIView):
#     serializer_class = TemplateSearchSerializer
#
#     def get_queryset(self):
#         queryset = Template.objects.filter(flag='public')
#         if self.kwargs.get('name'):
#             queryset = queryset.filter(name__contains='name')
#         if self.kwargs.get('des'):
#             queryset = queryset.filter(description__contains='des')
#         return queryset
