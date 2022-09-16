from django.urls import re_path

from . import apis

# from django.urls import path

urlpatterns = [
    # path('^signup/$', apis.signup),
    re_path('^login/$', apis.login),
    # url('^resend-otp/$', apis.resend_otp),
    # url('^verify-otp/$', apis.verify_otp),
    # url('^forget-password/$', apis.forget_password),
    # url('^reset-password/$', apis.reset_password),
    # url('^toggle-account-status/$', apis.toggle_account_status),
]
