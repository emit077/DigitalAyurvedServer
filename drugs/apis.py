import json

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators
from master.models import MasterVendorData
from .models import DrugData, PurchaseOrderData, PurchaseItemData
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
    anupaan = request.data.get(keys.ANUPAAN, None)
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
    drug_instance.anupaan = anupaan
    drug_instance.formulation = formulation
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
        keys.ANUPAAN: drug_instance.anupaan,
        keys.FORMULATION: drug_instance.formulation,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def purchase_order(request):
    vendor_table_id = request.data.get(keys.VENDOR_TABLE_ID, None)
    purchase_order_table_id = request.data.get(keys.PURCHASE_ORDER_TABLE_ID, None)
    invoice_id = request.data.get(keys.INVOICE_ID, None)
    invoice_date = request.data.get(keys.INVOICE_DATE, None)
    comment = request.data.get(keys.COMMENT, None)
    item_list = request.data.get(keys.ITEM_LIST, None)

    try:
        vendor = MasterVendorData.objects.get(id=vendor_table_id)
    except MasterVendorData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.NOT_FOUND_DYNAMIC.format(msg="Vendor")
        }, status=status.HTTP_400_BAD_REQUEST)

    if purchase_order_table_id:
        try:
            purchase_order_instance = PurchaseOrderData.objects.get(id=purchase_order_table_id)
            # delete all the item before editing the record
            PurchaseItemData.objects.filter(purchase_order=purchase_order_instance).delete()
        except PurchaseOrderData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        purchase_order_instance = DrugData()

    purchase_order_instance.vendor = vendor
    purchase_order_instance.invoice_id = invoice_id
    purchase_order_instance.invoice_date = invoice_date
    purchase_order_instance.comment = comment
    purchase_order_instance.save()

    if item_list and isinstance(item_list, str):
        item_list = json.loads(item_list)
        if item_list:
            for item in item_list:
                try:
                    drug_instance = DrugData.objects.get(id=item['drug'])
                    PurchaseItemData.objects.create(
                        purchase_order=purchase_order_instance,
                        drug=drug_instance,
                        qty=item['qty'],
                        purchase_price=item['purchase_price'],
                        mrp=item['mrp'],
                        expiry_date=item['expiry_date'],
                    )
                except DrugData.DoesNotExist:
                    return Response({
                        keys.SUCCESS: False,
                        keys.MESSAGE: messages.NOT_FOUND_DYNAMIC.format(msg="Drug")
                    }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.PURCHASE_ORDER_TABLE_ID: purchase_order_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def delete_purchase_order(request):
    purchase_order_table_id = request.data.get(keys.PURCHASE_ORDER_TABLE_ID, None)

    try:
        purchase_order_instance = PurchaseOrderData.objects.get(id=purchase_order_table_id)
        # delete all the item before editing the record
        PurchaseItemData.objects.filter(purchase_order=purchase_order_instance).delete()
        purchase_order_instance.delete()
    except PurchaseOrderData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.NOT_FOUND_DYNAMIC.format(msg="Purchase Order")
        }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
    }
    return Response(response, status=status.HTTP_200_OK)
