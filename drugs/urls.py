from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^add/$', apis.add_drugs),
    re_path('^list/$', apis.list_drug),
    re_path('^details/$', apis.drug_details),
    re_path('^delete/$', apis.delete_drug),
]
