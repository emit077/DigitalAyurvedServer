from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^vendor-list/$', apis.list_vendor),
]
