from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^template/(?P<uuid>[^/]+)$',
        views.import_template,
        name='template')
]