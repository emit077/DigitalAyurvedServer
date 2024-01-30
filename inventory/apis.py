import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators, CommonHelper
from master.models import MasterVendorData
from patient.models import PatientsData
from .models import DrugData, OrderData, OrderDetailsData
from .serializers import InOutItemDataSerializer

Users = get_user_model()


# @api_view(['POST'])
# @CustomDjangoDecorators.validate_access_token
# def delete_drug(request):
#     drug_table_id = request.data.get(keys.DRUG_TABLE_ID, None)
#     if drug_table_id:
#         try:
#             drug_instance = DrugData.objects.get(id=drug_table_id)
#             drug_instance.delete()
#         except DrugData.DoesNotExist:
#             return Response({
#                 keys.SUCCESS: False,
#                 keys.MESSAGE: messages.RECORD_NOT_FOUND
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#     response = {
#         keys.SUCCESS: True,
#         keys.MESSAGE: messages.SUCCESS,
#         keys.DRUG_TABLE_ID: drug_instance.id,
#     }
#     return Response(response, status=status.HTTP_200_OK)

#
# @api_view(['GET'])
# @CustomDjangoDecorators.validate_access_token
# def drug_details(request):
#     drug_table_id = request.GET.get(keys.DRUG_TABLE_ID, None)
#
#     try:
#         drug_instance = DrugData.objects.get(id=drug_table_id)
#     except DrugData.DoesNotExist:
#         return Response({
#             keys.SUCCESS: False,
#             keys.MESSAGE: messages.RECORD_NOT_FOUND
#         }, status=status.HTTP_400_BAD_REQUEST)
#
#     response = {
#         keys.SUCCESS: True,
#         keys.MESSAGE: messages.SUCCESS,
#         keys.DRUG_TABLE_ID: drug_instance.id,
#         keys.DRUG_NAME: drug_instance.drug_name,
#         keys.FORMULA: drug_instance.formula,
#         keys.BRAND: drug_instance.brand,
#         keys.DRUG_UNIT: drug_instance.drug_unit,
#         keys.ANUPAAN: drug_instance.anupaan,
#         keys.FORMULATION: drug_instance.formulation,
#     }
#     return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def create_purchase_order(request):
    vendor_table_id = request.data.get(keys.VENDOR_TABLE_ID, None)
    patient_table_id = request.data.get(keys.PATIENT_TABLE_ID, None)
    order_item_list = request.data.get(keys.ORDER_ITEM_LIST, None)
    transaction_type = request.data.get(keys.TRANSACTION_TYPE, None)
    comment = request.data.get(keys.COMMENT, None)
    print("request.data=>",request.data.get(keys.TRANSACTION_TYPE, None))
    # creating the purchase order
    if transaction_type == keys.PURCHASE_ORDER:
        try:
            vendor_instance = MasterVendorData.objects.get(id=vendor_table_id)
        except MasterVendorData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

        order_instance = OrderData.objects.create(
            vendor=vendor_instance,
            transaction_type=transaction_type,
            order_date=timezone.now()
        )

    # creating Sells Order
    elif transaction_type == keys.SALES_ORDER:
        try:
            patients_instance = PatientsData.objects.get(id=patient_table_id)
        except PatientsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

        order_instance = OrderData.objects.create(
            patient=patients_instance,
            transaction_type=transaction_type,
            order_date=timezone.now()
        )
    else:
        order_instance = OrderData.objects.create(
            transaction_type=transaction_type,
            comment=comment,
            order_date=timezone.now()
        )

    if order_item_list and isinstance(order_item_list, str):
        order_item_list = json.loads(order_item_list)
        for item in order_item_list:
            print("item==", item)

            drug = DrugData.objects.get(id=item["drug"])
            OrderDetailsData.objects.create(
                drug=drug,
                order_data=order_instance,
                quantity=item["qty"],
                expiry_date=item["expiry_date"],
                unit_price=item["unit_price"]
            )

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_purchase_order(request):
    search_query = request.GET.get(keys.SEARCH_QUERY, None)
    queryset = OrderData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(
            Q(vendor__vendor_name__icontains=search_query) |
            Q(vendor__contact_number__icontains=search_query))
    # pagination
    queryset, total_page_count = CommonHelper.do_pagination(queryset, request)
    purchase_order_list = InOutItemDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: total_page_count,
        keys.PURCHASE_ORDER_LIST: purchase_order_list,
    }
    return Response(response, status=status.HTTP_200_OK)
