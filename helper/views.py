# Create your views here.
from functools import wraps

import pytz
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pyotp import random_base32, TOTP
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

import keys
import messages
from DigitalAyurved.settings import TIME_ZONE


class HelperAuthentication:
    @staticmethod
    def get_token(user):
        """
        Method used to obtain a new token
        :param request: user instance
        :return:
        """
        print("get Token")
        try:
            token = Token.objects.get(user=user)
        except:
            return None
        return token.key

    @staticmethod
    def refresh_token(user):
        """
        Method used to refresh token
        :param : user instance
        :return:
        """
        try:
            token = Token.objects.get(user=user)
            token.delete()
            Token.objects.create(user=user)
        except:
            Token.objects.create(user=user)

        return token.key

    @staticmethod
    def verify_token(request):
        """
        Method used to verify the token
        :return:
        """
        print("request==")
        print(request.headers)
        try:
            token = request.headers[keys.ACCESS_TOKEN]
            if Token.objects.filter(key=token).exists():
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def get_users_instance(request):
        """
        Method used to verify the token
        :return:
        """
        try:
            token = request.headers[keys.ACCESS_TOKEN]
            instance = Token.objects.get(key=token)
            return instance.user
        except:
            return None

    @staticmethod
    def generate_otp_token():
        """
        Generates a random OTP token to use later for verification.
        :return: random base32 OTP token
        """
        return random_base32()

    @staticmethod
    def send_otp(secret, mobile):
        otp = TOTP(secret, digits=keys.OTP_LENGTH).now()
        sms = messages.OTP_FORMAT.format(otp=otp, text="TF")
        print("send_otp==", otp)
        print("mobile==", mobile)
        # send_sms(mobile=mobile, otp=otp)
        # send_sms(mobile=mobile, sms=sms, template_id="1007164710745702774")
        return ''

    @staticmethod
    def verify_otp(otp, secret):
        return TOTP(secret, digits=keys.OTP_LENGTH).verify(otp, valid_window=4)


class CustomDjangoDecorators:
    """
    Define all the custom decorators here.
    """

    @staticmethod
    def validate_access_token(function):
        """
        Custom decorator to verify user access token
        """

        @wraps(function)
        def wrap(request, *args, **kwargs):
            res = HelperAuthentication.verify_token(request)
            if not res:
                return Response(data={keys.SUCCESS: False, keys.MESSAGE: messages.INVALID_TOKEN},
                                status=status.HTTP_403_FORBIDDEN)
            return function(request, *args, **kwargs)

        return wrap


class CommonHelper:

    @staticmethod
    def get_city(request):
        city_id = 1
        return "Bhilai"

    @staticmethod
    def convert_utc_to_local_timezone(datetime_instance):
        """
        Used to convert UTC timezone to local timezone defined in settings
        :param datetime_instance:
        :return:
        """
        return datetime_instance.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE))

    @staticmethod
    def calc_subscription_price(number_of_students, number_of_installments, base_price):
        base_price = float(base_price)
        if int(number_of_students) > 1:
            price = base_price + (base_price / 2)
            return round(price / float(number_of_installments), 2)
        else:
            return round(base_price / float(number_of_installments), 2)

    @staticmethod
    def generate_id(id, prefix):
        for i in range(10 - (len(str(id)) + len(prefix))):
            prefix += "0"
        return prefix + str(id)

    @staticmethod
    def amount_format(amount, is_round=False):
        if is_round:
            return '{:2.2f}'.format(round(float(amount)))
        else:
            return '{:2.2f}'.format(float(amount))

    @staticmethod
    def do_pagination(queryset, request):
        page_number = request.GET.get(keys.PAGE_NUMBER, 1)
        page_length = request.GET.get(keys.PAGE_LENGTH, 20)
        paginator = Paginator(queryset, page_length)
        try:
            queryset = paginator.page(page_number)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset, paginator.num_pages

    # @staticmethod
    # def send_email(to, email, subject, body, show_login_btn=False):
    #     data_dict = {"data": {
    #         "name": to.upper(),
    #         "body": body,
    #         "show_login_btn": show_login_btn,
    #     }}
    #     template = get_template('reg_email-template.html')
    #     html = template.render(data_dict)
    #     send_email(to=email, subject=subject, content=html)
