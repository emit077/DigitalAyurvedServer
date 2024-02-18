import json
import os
from datetime import datetime, timedelta

import pdfkit
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from num2words import num2words
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from drugs.serializers import DrugDataSerializer
from helper.views import CustomDjangoDecorators, CommonHelper, CalculationHelper
from inventory.models import DrugData, OrderData, OrderDetailsData, InvoiceDetailsData, InvoiceData
from master.models import MasterVendorData
from patient.models import PatientsData, TreatmentRecord
from .serializers import OrderDataSerializer, InvoiceDataSerializer, InvoiceDetailsDataSerializer, \
    OrderDetailsAutocompleteSerializer
from .views import update_available_item

Users = get_user_model()


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def dashboard_overview(request):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    today_sales = InvoiceData.objects.filter(invoice_date=datetime.today()).aggregate(Sum('invoice_total'))[
                      "invoice_total__sum"] or 0

    monthly_sales = \
        InvoiceData.objects.filter(invoice_date__range=[start_date, end_date]).aggregate(Sum('invoice_total'))[
            "invoice_total__sum"] or 0

    today_patient = TreatmentRecord.objects.filter(created=datetime.today()).count()
    monthly_patient = TreatmentRecord.objects.filter(created__range=[start_date, end_date]).count()

    queryset = DrugData.objects.all()

    queryset = queryset.annotate(
        quantity=Coalesce(Sum('invoice_drug__quantity'), 0, output_field=FloatField()))

    queryset = queryset.annotate(
        amount=Coalesce(Sum(F('invoice_drug__quantity') * F("invoice_drug__selling_price")), 0,
                        output_field=FloatField()))

    best_sellers = queryset.order_by("-quantity")[:5].values("drug_name", "amount", "quantity")

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TODAY_SALES: today_sales,
        keys.MONTHLY_SALES: monthly_sales,
        keys.TODAY_PATIENT: today_patient,
        keys.MONTHLY_PATIENT: monthly_patient,
        keys.BEST_SELLERS: best_sellers,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def inventory_overview(request):
    queryset = DrugData.objects.all().order_by('-id')

    queryset = queryset.annotate(
        available_qty=Coalesce(Sum('purchase_drug__available_qty'), 0, output_field=FloatField()))

    near_stock_out = DrugDataSerializer(queryset.filter(available_qty__gt=0).order_by('available_qty')[:5],
                                        many=True).data
    stock_out = DrugDataSerializer(queryset.filter(available_qty=0)[:5], many=True).data

    near_expiry = OrderDetailsAutocompleteSerializer(
        OrderDetailsData.objects.filter(expiry_date__gt=datetime.today()).order_by("expiry_date")[:5], many=True).data
    expired = OrderDetailsAutocompleteSerializer(
        OrderDetailsData.objects.filter(expiry_date__lte=datetime.today()).order_by("-expiry_date")[:5], many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.NEAR_STOCK_OUT: near_stock_out,
        keys.STOCK_OUT: stock_out,
        keys.NEAR_EXPIRY: near_expiry,
        keys.EXPIRED: expired,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def create_purchase_order(request):
    vendor_table_id = request.data.get(keys.VENDOR_TABLE_ID, None)
    order_item_list = request.data.get(keys.ORDER_ITEM_LIST, None)
    transaction_type = request.data.get(keys.TRANSACTION_TYPE, None)
    comment = request.data.get(keys.COMMENT, None)
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
    item_total = 0
    if order_item_list and isinstance(order_item_list, str):
        order_item_list = json.loads(order_item_list)

        for item in order_item_list:
            # drug = DrugData.objects.get(id=item["drug"])
            drug = DrugData.objects.get(id=int(item["drug"]["drug_table_id"]))
            # calculating the discount and discounted price
            item_total = float(item["qty"]) * float(item["unit_price"]) + item_total

            OrderDetailsData.objects.create(
                drug=drug,
                order_data=order_instance,
                quantity=item["qty"],
                available_qty=item["qty"],
                expiry_date=item["expiry_date"],
                unit_price=item["unit_price"],
                mrp=item["mrp"],
            )
    order_instance.order_total = item_total
    order_instance.save()
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
    purchase_order_list = OrderDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: total_page_count,
        keys.PURCHASE_ORDER_LIST: purchase_order_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def sales_drug_list(request):
    search_query = request.GET.get(keys.SEARCH_QUERY, None)
    queryset = OrderDetailsData.objects.filter(available_qty__gt=0).order_by('drug__drug_name', 'expiry_date')

    if search_query:
        queryset = queryset.filter(
            Q(drug__drug_name__icontains=search_query) |
            Q(drug__id__icontains=search_query))
    # pagination
    queryset, total_page_count = CommonHelper.do_pagination(queryset, request)
    drug_list = OrderDetailsAutocompleteSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: total_page_count,
        keys.DRUG_LIST: drug_list,
    }
    return Response(response, status=status.HTTP_200_OK)


# Invoice APIs
# ---------------------------------------------------------------
@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def create_invoice(request):
    invoice_table_id = request.data.get(keys.INVOICE_TABLE_ID, None)
    patient_table_id = request.data.get(keys.PATIENT_TABLE_ID, None)
    order_item_list = request.data.get(keys.ORDER_ITEM_LIST, None)
    discount_value = request.data.get(keys.DISCOUNT_VALUE, None)

    try:
        patients_instance = PatientsData.objects.get(id=int(patient_table_id))
    except PatientsData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    if invoice_table_id:
        try:
            invoice_instance = InvoiceData.objects.get(id=int(invoice_table_id))
            # find and delete all the records and create new records
            for item in InvoiceDetailsData.objects.filter(invoice_data=invoice_instance):
                update_available_item(item, keys.IN)
                item.delete()

        except InvoiceData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        invoice_instance = InvoiceData.objects.create(
            patient=patients_instance,
            invoice_date=timezone.now()
        )
    invoice_total = 0
    total_discount = 0
    invoice_item_total = 0
    if order_item_list and isinstance(order_item_list, str):
        for item in json.loads(order_item_list):
            # calculating the discount and discounted price
            item_total = float(item["qty"]) * float(item["drug"]["mrp"])
            discount_amount = CalculationHelper.cal_discount(item_total, discount_value)

            invoice_total = invoice_total + (item_total - discount_amount)
            total_discount = total_discount + discount_amount
            invoice_item_total = invoice_item_total + item_total

            invoice_item = InvoiceDetailsData.objects.create(
                drug=DrugData.objects.get(id=int(item["drug"]["drug_table_id"])),
                order_items=OrderDetailsData.objects.get(id=int(item["drug"]["order_items_table_id"])),
                invoice_data=invoice_instance,
                quantity=item["qty"],
                selling_price=round((item_total - discount_amount) / float(item["qty"]), 2),
                mrp=float(item["drug"]["mrp"])
            )
            update_available_item(invoice_item, keys.OUT)

    # update the invoice data
    round_off_amt = CalculationHelper.cal_round_off(invoice_total)
    invoice_instance.round_off = round_off_amt
    invoice_instance.invoice_total = invoice_total + round_off_amt
    invoice_instance.item_total = invoice_item_total
    invoice_instance.discount_amount = total_discount
    invoice_instance.discount_value = discount_value
    invoice_instance.discount_type = keys.PERCENT_DISCOUNT
    invoice_instance.save()

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.INVOICE_TABLE_ID: invoice_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_invoice(request):
    search_query = request.GET.get(keys.SEARCH_QUERY, None)
    queryset = InvoiceData.objects.all().order_by('-id')

    if search_query:
        queryset = queryset.filter(
            Q(invoice_id__icontains=search_query) |
            Q(patient__patient_first_name__icontains=search_query) |
            Q(patient__user__mobile__icontains=search_query) |
            Q(patient__patient_id__icontains=search_query))

    # pagination
    queryset, total_page_count = CommonHelper.do_pagination(queryset, request)
    invoice_list = InvoiceDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: total_page_count,
        keys.INVOICE_LIST: invoice_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def get_invoice_details(request):
    invoice_table_id = request.GET.get(keys.INVOICE_TABLE_ID, None)

    try:
        invoice_instance = InvoiceData.objects.get(id=invoice_table_id)
    except InvoiceData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    invoice_details_instance = InvoiceDetailsData.objects.filter(invoice_data=invoice_instance)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.INVOICE_DATA: InvoiceDataSerializer(invoice_instance, many=False).data,
        keys.INVOICE_ITEMS: InvoiceDetailsDataSerializer(invoice_details_instance, many=True).data,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_invoice(request):
    invoice_table_id = request.GET.get(keys.INVOICE_TABLE_ID)

    logo_url = ""  # request.build_absolute_uri(MasterImageData.objects.get(name='invoice_logo').image.url)

    try:
        invoice_data = InvoiceData.objects.get(id=invoice_table_id)
    except:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.SUBSCRIPTION_PLAN_NOT_FOUND
        }, status=status.HTTP_200_OK)

    data_dict = {"data": {
        "item_total": CommonHelper.amount_format(invoice_data.item_total),
        "invoice_total": CommonHelper.amount_format(invoice_data.invoice_total),
        "discount_amount": CommonHelper.amount_format(invoice_data.discount_amount),
        "discount_value": CommonHelper.amount_format(invoice_data.discount_value),
        "round_off": CommonHelper.amount_format(invoice_data.round_off),
        "invoice_total_in_words": num2words(invoice_data.invoice_total, lang='en_IN').title() + " Rupees Only.",

        "patient_name": invoice_data.patient.patient_name() if invoice_data.patient else "",
        "patient_mobile": invoice_data.patient.user.mobile if invoice_data.patient else "",
        "patient_address": invoice_data.patient.address if invoice_data.patient else "",

        "invoice_id": invoice_data.invoice_id,
        "invoice_date": invoice_data.invoice_date.strftime(keys.DATE_FORMAT),
        "company_email": keys.COMPANY_EMAIL,
        "company_mobile": keys.COMPANY_MOBILE,
        "company_website": keys.COMPANY_WEBSITE,
        "logo_url": logo_url,
        "invoice_items": InvoiceDetailsData.objects.filter(invoice_data=invoice_data),

    }}
    template = get_template('pdf-templates/invoice_template.html')
    html = template.render(data_dict)

    options = {
        'page-size': 'A4',
        'margin-top': '0.4in',
        'margin-right': '0.4in',
        'margin-bottom': '0.4in',
        'margin-left': '0.4in',
    }

    pdfkit.from_string(html, 'inventory/invoice.pdf', options=options)
    pdf = open("inventory/invoice.pdf", 'rb')
    response = HttpResponse(pdf.read(), content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename=invoice.pdf'
    pdf.close()
    os.remove("inventory/invoice.pdf")
    return response
