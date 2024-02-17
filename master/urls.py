from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^vendor-list/$', apis.list_vendor),
    re_path('^brand-list/$', apis.list_brand),
    re_path('^formulation-list/$', apis.list_formulation_type),
]
