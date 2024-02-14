from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators
from .models import EnquiryData
from .serializers import EnquiryDataSerializer

Users = get_user_model()


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def add_enquiry(request):
    name = request.data.get(keys.NAME, None)
    mobile = request.data.get(keys.MOBILE, None)
    email = request.data.get(keys.EMAIL, None)
    message = request.data.get(keys.MESSAGE, None)

    EnquiryData.objects.create(
        name=name,
        mobile=mobile,
        email=email,
        message=message
    )
    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_enquiry(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = EnquiryData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(
            Q(name__istartswith=search_query) |
            Q(mobile__icontains=search_query) |
            Q(email__icontains=search_query))

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    enquiry_list = EnquiryDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.ENQUIRY_LIST: enquiry_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def enquiry_details(request):
    patient_table_id = request.GET.get(keys.PATIENT_TABLE_ID, None)
    try:
        enquiry_instance = EnquiryData.objects.get(id=patient_table_id)
    except EnquiryData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        # keys.MESSAGE: messages.SUCCESS,
        keys.NAME: enquiry_instance.name,
        keys.MOBILE: enquiry_instance.mobile,
        keys.EMAIL: enquiry_instance.email,
        keys.MESSAGE: enquiry_instance.message,
    }
    return Response(response, status=status.HTTP_200_OK)
