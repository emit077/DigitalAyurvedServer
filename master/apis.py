from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators
from .models import MasterVendorData, MasterBrandData, MasterFormulationData
from .serializers import VendorDataSerializer, MasterBrandDataSerializer, MasterFormulationDataSerializer

Users = get_user_model()


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_vendor(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = MasterVendorData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(
            Q(user__name__istartswith=search_query) |
            Q(user__mobile__icontains=search_query) |
            Q(user__email__icontains=search_query))

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    vendor_list = VendorDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.VENDOR_LIST: vendor_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_brand(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = MasterBrandData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(brand_name__istartswith=search_query)

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    brand_list = MasterBrandDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.BRAND_LIST: brand_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_formulation_type(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = MasterFormulationData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(formulation_type__istartswith=search_query)

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    formulation_list = MasterFormulationDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.FORMULATION_LIST: formulation_list,
    }
    return Response(response, status=status.HTTP_200_OK)
