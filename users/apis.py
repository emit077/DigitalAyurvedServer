from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import HelperAuthentication

Users = get_user_model()


@api_view(['POST'])
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def login(request):
    """
        mobile -- mobile number is required
        password -- password is required
    """
    mobile = request.data.get(keys.MOBILE, None)
    password = request.data.get(keys.PASSWORD, None)

    print(Users.objects.filter(mobile=mobile))
    if not Users.objects.filter(mobile=mobile).exists():
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.MOBILE_NUMBER_NOT_REGISTER
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Users.objects.get(mobile=mobile)
    except ObjectDoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.MOBILE_NUMBER_NOT_REGISTER
        }, status=status.HTTP_400_BAD_REQUEST)

    #  check password
    # if not check_password(password, user.password):
    #     return Response({
    #         keys.SUCCESS: False,
    #         keys.MESSAGE: messages.INVALID_CREDENTIALS
    #     }, status=status.HTTP_400_BAD_REQUEST)
    # else:
    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.ACCOUNT_TYPE: user.account_type,
        # keys.NAME: user.name,
        # keys.IS_OTP_VERIFIED: user.is_otp_verified,
    }
    headers = {
        keys.ACCESS_TOKEN: HelperAuthentication.get_token(user)
    }

    return Response(response, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST'])
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def signup(request):
    """
        signup for both tutor/student
        mobile -- mobile number is required
        password -- password is required
    """
    name = request.data.get(keys.NAME, None)
    mobile = request.data.get(keys.MOBILE, None)
    email = request.data.get(keys.EMAIL, None)
    password = request.data.get(keys.PASSWORD, None)
    account_type = request.data.get(keys.ACCOUNT_TYPE, None)

    if Users.objects.filter(mobile=mobile).exists():
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.MOBILE_ALREADY_EXIST
        }, status=status.HTTP_200_OK)

    """ crating the user object """
    user = Users.objects.create(
        mobile=mobile,
        email=email,
        name=name,
        account_type=account_type,
        is_account_active=True,
    )
    user.set_password(password)
    user.save()

    """ send otp to the user """
    if not user:
        user = Users.objects.get(mobile=mobile)
    user.otp_token = HelperAuthentication.generate_otp_token()
    user.save()
    otp = HelperAuthentication.send_otp(user.otp_token, user.mobile)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.OTP: otp,
        keys.ACCOUNT_TYPE: user.account_type,
        keys.NAME: user.name,
    }
    headers = {
        keys.OTP_TOKEN: user.otp_token
    }
    return Response(response, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST'])
def resend_otp(request):
    otp_token = request.headers[keys.OTP_TOKEN]
    try:
        user = Users.objects.get(otp_token=otp_token)
        was_limited = getattr(request, 'limited', False)
        if not was_limited:
            HelperAuthentication.send_otp(user.otp_token, str(user.mobile))
        else:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.USER_RESEND_OTP_LIMIT_REACHED
            }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.USER_INVALID_OTP_TOKEN
        }, status=status.HTTP_403_FORBIDDEN)
    return Response({
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_otp(request):
    """
    verify otp api ¬
    """
    otp_token = request.headers[keys.OTP_TOKEN]
    otp = request.POST.get(keys.OTP)
    try:
        user = Users.objects.get(otp_token=otp_token)
        if not HelperAuthentication.verify_otp(otp, otp_token):
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.INVALID_OTP
            }, status=status.HTTP_200_OK)
        else:
            user.is_otp_verified = True
            user.save()
    except ObjectDoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.USER_INVALID_OTP_TOKEN
        }, status=status.HTTP_403_FORBIDDEN)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.NAME: user.name,
        keys.ACCOUNT_TYPE: user.account_type
    }
    headers = {
        keys.ACCESS_TOKEN: HelperAuthentication.get_token(user),
    }
    return Response(response, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST'])
def forget_password(request):
    """
    forget password api
    """
    mobile = request.POST.get(keys.MOBILE)

    try:
        user = Users.objects.get(mobile=mobile)
        user.otp_token = HelperAuthentication.generate_otp_token()
        user.save()
        otp = HelperAuthentication.send_otp(user.otp_token, user.mobile)
    except ObjectDoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.USER_NOT_FOUND
        }, status=status.HTTP_200_OK)

    headers = {
        keys.OTP_TOKEN: user.otp_token,
    }
    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.OTP: otp
    }

    return Response(response, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST'])
def reset_password(request):
    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS
    }
    password = request.POST.get(keys.PASSWORD)

    try:
        user = HelperAuthentication.get_users_instance(request)
        print(user.mobile)
        user.set_password(password)
        user.save()
        response[keys.MESSAGE] = messages.SUCCESS
    except ObjectDoesNotExist:
        response[keys.SUCCESS] = False
        response[keys.MESSAGE] = messages.USER_NOT_FOUND

    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def toggle_account_status(request):
    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS
    }
    print(request.data)
    user_table_id = request.POST.get(keys.USER_TABLE_ID)
    try:
        user = Users.objects.get(id=user_table_id)
        user.is_active = not user.is_active
        user.save()
        print("user.is_active::", user.is_active)
    except ObjectDoesNotExist:
        response[keys.SUCCESS] = False
        response[keys.MESSAGE] = messages.USER_NOT_FOUND

    return Response(response, status=status.HTTP_200_OK)
