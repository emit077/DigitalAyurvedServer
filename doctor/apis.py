import keys
import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DoctorsData
from .serializers import DoctorDataSerializer
from helper.views import CustomDjangoDecorators

Users = get_user_model()


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def add_doctor(request):
    """
        doctor registration / edit doctor profile
        mobile -- mobile number is required
        password -- password is required
    """
    print(request.data)
    name = request.data.get(keys.NAME, None)
    mobile = request.data.get(keys.MOBILE, None)
    email = request.data.get(keys.EMAIL, None)
    degree = request.data.get(keys.DEGREE, None)
    dob = request.data.get(keys.DOB, None)
    gender = request.data.get(keys.GENDER, None)
    medical_reg_no = request.data.get(keys.MEDICAL_REG_NO, None)
    designation = request.data.get(keys.DESIGNATION, None)
    address = request.data.get(keys.ADDRESS, None)
    city = request.data.get(keys.CITY, None)
    doctor_table_id = request.data.get(keys.DOCTOR_TABLE_ID, None)
    password = request.data.get(keys.PASSWORD, None)

    if doctor_table_id:
        try:
            doctor_instance = DoctorsData.objects.get(id=doctor_table_id)
            user_instance = doctor_instance.user
            user_instance.mobile = mobile
            user_instance.email = email
            user_instance.name = name
            user_instance.save()
        except DoctorsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        if Users.objects.filter(mobile=mobile).exists():
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.MOBILE_ALREADY_EXIST
            }, status=status.HTTP_400_BAD_REQUEST)

        user_instance = Users.objects.create(
            mobile=mobile,
            email=email,
            name=name,
            account_type=keys.ACCOUNT_DOCTOR
        )
        doctor_instance = DoctorsData()
        doctor_instance.user = user_instance

    doctor_instance.degree = degree
    doctor_instance.medical_reg_no = medical_reg_no
    doctor_instance.designation = designation
    doctor_instance.address = address
    doctor_instance.city = city
    doctor_instance.dob = dob
    doctor_instance.gender = gender

    doctor_instance.save()
    if password:
        user_instance.set_password(password)
        user_instance.save()

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DOCTOR_TABLE_ID: doctor_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_doctor(request):
    """
        :return-- list of doctors
    """
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = DoctorsData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(
            Q(user__name__istartswith=search_query) |
            Q(user__mobile__icontains=search_query) |
            Q(medical_reg_no__istartswith=search_query) |
            Q(user__email__icontains=search_query))

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    doctor_list = DoctorDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.DOCTOR_LIST: doctor_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def doctor_details(request):
    """
        :return-- doctors details
    """
    doctor_table_id = request.GET.get(keys.DOCTOR_TABLE_ID, None)

    try:
        doctor_instance = DoctorsData.objects.get(id=doctor_table_id)
    except DoctorsData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.NAME: doctor_instance.user.name,
        keys.MOBILE: doctor_instance.user.mobile,
        keys.EMAIL: doctor_instance.user.email,
        keys.GENDER: doctor_instance.gender,
        keys.DOB: doctor_instance.dob,
        keys.DEGREE: doctor_instance.degree,
        keys.MEDICAL_REG_NO: doctor_instance.medical_reg_no,
        keys.DESIGNATION: doctor_instance.designation,
        keys.ADDRESS: doctor_instance.address,
        keys.CITY: doctor_instance.city,
    }
    return Response(response, status=status.HTTP_200_OK)
