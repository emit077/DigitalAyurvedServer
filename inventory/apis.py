import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.template.loader import get_template
from django.utils import timezone
from num2words import num2words
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper.views import CustomDjangoDecorators, CommonHelper, CalculationHelper
from master.models import MasterVendorData
from patient.models import PatientsData
from .models import DrugData, OrderData, OrderDetailsData, InvoiceDetailsData, InvoiceData
from .serializers import OrderDataSerializer, InvoiceDataSerializer, InvoiceDetailsDataSerializer

Users = get_user_model()


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def create_purchase_order(request):
    vendor_table_id = request.data.get(keys.VENDOR_TABLE_ID, None)
    patient_table_id = request.data.get(keys.PATIENT_TABLE_ID, None)
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

    if order_item_list and isinstance(order_item_list, str):
        order_item_list = json.loads(order_item_list)

        for item in order_item_list:
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
    purchase_order_list = OrderDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: total_page_count,
        keys.PURCHASE_ORDER_LIST: purchase_order_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def create_invoice(request):
    patient_table_id = request.data.get(keys.PATIENT_TABLE_ID, None)
    order_item_list = request.data.get(keys.ORDER_ITEM_LIST, None)
    discount_value = request.data.get(keys.DISCOUNT_VALUE, None)
    discount_type = request.data.get(keys.DISCOUNT_TYPE, None)
    comment = request.data.get(keys.COMMENT, None)

    try:
        patients_instance = PatientsData.objects.get(id=patient_table_id)
    except PatientsData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    invoice_instance = InvoiceData.objects.create(
        patient=patients_instance,
        invoice_date=timezone.now()
    )
    invoice_total = 0
    total_discount = 0
    invoice_item_total = 0
    if order_item_list and isinstance(order_item_list, str):
        for item in json.loads(order_item_list):
            drug = DrugData.objects.get(id=item["drug"])
            # calculating the discount and discounted price
            item_total = float(item["qty"]) * float(item["unit_price"])
            discount_amount = CalculationHelper.cal_discount(item_total, discount_value)

            invoice_total = invoice_total + (item_total - discount_amount)
            total_discount = total_discount + discount_amount
            invoice_item_total = invoice_item_total + item_total

            # print("item[""])==", item["qty"], item["unit_price"], "=", item_total)
            # print("discount_amount==", discount_amount)

            InvoiceDetailsData.objects.create(
                drug=drug,
                invoice_data=invoice_instance,
                quantity=item["qty"],
                expiry_date=item["expiry_date"],
                selling_price=round((item_total - discount_amount) / float(item["qty"]), 2),
                mrp=0
            )

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
            Q(patient__first_name__icontains=search_query) |
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

    # try:
    invoice_instance = InvoiceData.objects.get(id=invoice_table_id)
    # except InvoiceData.DoesNotExist:
    #     return Response({
    #         keys.SUCCESS: False,
    #         keys.MESSAGE: messages.RECORD_NOT_FOUND
    #     }, status=status.HTTP_400_BAD_REQUEST)

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

    logo_url = request.build_absolute_uri(MasterImageData.objects.get(name='invoice_logo').image.url)
    print("logo_url==", logo_url)

    try:
        invoice_data = InvoiceData.objects.get(id=invoice_table_id)
    except:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.SUBSCRIPTION_PLAN_NOT_FOUND
        }, status=status.HTTP_200_OK)

    payment_list = []
    total_paid = 0
    data_dict = {"data": {
        "item_total": CommonHelper.amount_format(invoice_data.item_total),
        "invoice_total": CommonHelper.amount_format(invoice_data.invoice_total),
        "discount_amount": CommonHelper.amount_format(invoice_data.discount_amount),  # inclusive tax
        "discount_value": invoice_data,
        "round_off_amt": invoice_data,
        "buyer_mobile": invoice_data.patient.name() if invoice_data.patient else "",
        "buyer_email": invoice_data.patient.name() if invoice_data.patient else "",
        "buyer_address": invoice_data.patient.address if invoice_data.patient else "",
        "qty": 1,
        "rate": CommonHelper.amount_format(float(amount) + float(sub_data.discount_amount)),
        "invoice_number": CommonHelper.generate_id(sub_data.id, 'INV'),
        "invoice_date": sub_data.start_date.strftime(keys.DATE_FORMAT),
        "due_date": due_date,
        "gst_number": keys.GST_NUMBER,
        "company_email": keys.COMPANY_EMAIL,
        "company_mobile": keys.COMPANY_MOBILE,
        "company_website": keys.COMPANY_WEBSITE,
        "logo_url": logo_url,
        "payment_list": payment_list,
        "total_paid": CommonHelper.amount_format(total_paid),
        "total_due": CommonHelper.amount_format(sub_data.payable_amount - total_paid),
        "amount_in_words": num2words(int(sub_data.payable_amount)).title() + " Only",
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

    pdfkit.from_string(html, 'subscription/invoice.pdf', options=options)
    pdf = open("subscription/invoice.pdf", 'rb')
    response = HttpResponse(pdf.read(), content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename=invoice.pdf'
    pdf.close()
    os.remove("subscription/invoice.pdf")
    return response
