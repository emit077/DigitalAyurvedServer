from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators
from .models import DrugData
from .serializers import DrugDataSerializer

Users = get_user_model()


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def add_drugs(request):
    drug_table_id = request.data.get(keys.DRUG_TABLE_ID, None)
    drug_name = request.data.get(keys.DRUG_NAME, None)
    formula = request.data.get(keys.FORMULA, None)
    brand = request.data.get(keys.BRAND, None)
    drug_unit = request.data.get(keys.DRUG_UNIT, None)
    anupana = request.data.get(keys.ANUPANA, None)
    formulation = request.data.get(keys.FORMULATION, None)

    if drug_table_id:
        try:
            drug_instance = DrugData.objects.get(id=drug_table_id)
        except DrugData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        drug_instance = DrugData()

    drug_instance.drug_name = drug_name
    drug_instance.formula = formula
    drug_instance.brand = brand
    drug_instance.drug_unit = drug_unit
    drug_instance.anupana = anupana
    drug_instance.formulation = formulation

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DRUG_TABLE_ID: drug_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_drug(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = DrugData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(
            Q(drug_name__icontains=search_query) |
            Q(formula__icontains=search_query) |
            Q(brand__icontains=search_query))

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    drug_list = DrugDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.DRUG_LIST: drug_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def drug_details(request):
    drug_table_id = request.GET.get(keys.DRUG_TABLE_ID, None)

    try:
        drug_instance = DrugData.objects.get(id=drug_table_id)
    except DrugData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DRUG_TABLE_ID: drug_instance.id,
        keys.DRUG_NAME: drug_instance.drug_name,
        keys.FORMULA: drug_instance.formula,
        keys.BRAND: drug_instance.brand,
        keys.DRUG_UNIT: drug_instance.drug_unit,
        keys.ANUPANA: drug_instance.anupana,
        keys.FORMULATION: drug_instance.formulation,
    }
    return Response(response, status=status.HTTP_200_OK)
