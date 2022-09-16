from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^add/$', apis.add_patient),
    re_path('^list/$', apis.list_patient),
    re_path('^details/$', apis.patient_details),
    re_path('^add/prescription/$', apis.add_prescription),
    re_path('^get/treatment-details/$', apis.get_prescription_details),
    re_path('^get/prescription-supporting-data/$', apis.get_prescription_supporting_data),
]
