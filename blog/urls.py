from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    re_path('^list/$', apis.blog_list),
    re_path('^details/$', apis.blog_details),
]
