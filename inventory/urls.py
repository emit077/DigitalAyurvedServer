from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^create-purchase-order/$', apis.create_purchase_order),
    re_path('^list-purchase-order/$', apis.list_purchase_order),
]
