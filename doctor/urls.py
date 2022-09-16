from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^add/$', apis.add_doctor),
    re_path('^list/$', apis.list_doctor),
    re_path('^details/$', apis.doctor_details),
]
