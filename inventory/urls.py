from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^create-purchase-order/$', apis.create_purchase_order),
    re_path('^list-purchase-order/$', apis.list_purchase_order),
    re_path('^list-sales-drugs/$', apis.sales_drug_list),
    re_path('^create-invoice/$', apis.create_invoice),
    re_path('^list-invoice/$', apis.list_invoice),
    re_path('^get-invoice-details/$', apis.get_invoice_details),
    re_path('^get-invoice/$', apis.get_invoice),
]
