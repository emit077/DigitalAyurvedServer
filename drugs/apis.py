from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators, CommonHelper
from master.models import MasterBrandData, MasterFormulationData
from .models import DrugData
from .serializers import DrugDataSerializer

Users = get_user_model()


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def add_drugs(request):
    drug_table_id = request.data.get(keys.DRUG_TABLE_ID, None)
    drug_name = request.data.get(keys.DRUG_NAME, None)
    formula = request.data.get(keys.FORMULA, None)
    brand_table_id = request.data.get(keys.BRAND_TABLE_ID, None)
    formulation_table_id = request.data.get(keys.FORMULATION_TABLE_ID, None)

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
    drug_instance.brand = MasterBrandData.objects.get(id=brand_table_id)
    drug_instance.formulation = MasterFormulationData.objects.get(id=formulation_table_id)
    drug_instance.save()

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DRUG_TABLE_ID: drug_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def delete_drug(request):
    drug_table_id = request.data.get(keys.DRUG_TABLE_ID, None)
    if drug_table_id:
        try:
            drug_instance = DrugData.objects.get(id=drug_table_id)
            drug_instance.delete()
        except DrugData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DRUG_TABLE_ID: drug_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_drug(request):
    search_query = request.GET.get(keys.SEARCH_QUERY, None)
    type = request.GET.get(keys.TYPE, None)

    queryset = DrugData.objects.all().order_by('-id')

    queryset = queryset.annotate(
        available_qty=Sum('purchase_drug__available_qty', filter=Q(purchase_drug__available_qty__gt=0)))

    if type == keys.STOCK_OUT:
        queryset = queryset.filter(available_qty=0)
    elif type == keys.NEAR_STOCK_OUT:
        queryset = queryset.filter(available_qty__gt=0).order_by('available_qty')

    if search_query:
        queryset = queryset.filter(
            Q(drug_name__icontains=search_query) |
            Q(formula__icontains=search_query) |
            Q(brand__icontains=search_query))
    # pagination
    queryset, total_page_count = CommonHelper.do_pagination(queryset, request)
    drug_list = DrugDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: total_page_count,
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
        keys.BRAND_NAME: drug_instance.brand.brand_name,
        keys.BRAND_TABLE_ID: drug_instance.brand.id,
        keys.FORMULATION_TABLE_ID: drug_instance.formulation_type.id if drug_instance.formulation_type else "",
        keys.FORMULATION: drug_instance.formulation_type.formulation_type if drug_instance.formulation_type else "",
    }
    return Response(response, status=status.HTTP_200_OK)
