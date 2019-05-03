from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^template/(?P<uuid>[^/]+)/$',
        views.share_template,
        name='share_template'),
    url(r'^search_template/$',
        views.search_template,
        name='search_template')
]