from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^add/$', apis.add_enquiry),
    re_path('^list/$', apis.list_enquiry),
    re_path('^details/$', apis.enquiry_details)
]
