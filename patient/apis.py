import json

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from doctor.models import DoctorsData
from drugs.models import DrugData
from helper.views import CustomDjangoDecorators, HelperAuthentication
from master.models import MaterDoseData, MaterFrequencyData, MaterInstructionData
from .models import PatientsData, TreatmentRecord, PrescriptionRecord
from .serializers import PatientsDataSerializer, PrescriptionRecordSerializer, TreatmentRecordSerializer

Users = get_user_model()


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def add_patient(request):
    patient_table_id = request.data.get(keys.PATIENT_TABLE_ID, None)
    patient_first_name = request.data.get(keys.PATIENT_FIRST_NAME, None)
    patient_last_name = request.data.get(keys.PATIENT_LAST_NAME, None)
    occupation = request.data.get(keys.OCCUPATION, None)
    age = request.data.get(keys.AGE, None)
    mobile = request.data.get(keys.MOBILE, None)
    email = request.data.get(keys.EMAIL, None)
    gender = request.data.get(keys.GENDER, None)
    address = request.data.get(keys.ADDRESS, None)
    city = request.data.get(keys.CITY, None)

    if patient_table_id:
        try:
            patients_instance = PatientsData.objects.get(id=patient_table_id)
            user_instance = patients_instance.user
            if mobile:
                user_instance.mobile = mobile
            user_instance.email = email
            user_instance.save()
        except PatientsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        patients_instance = PatientsData()
        if mobile:
            if Users.objects.filter(mobile=mobile).exists():
                return Response({
                    keys.SUCCESS: False,
                    keys.MESSAGE: messages.MOBILE_ALREADY_EXIST
                }, status=status.HTTP_400_BAD_REQUEST)

            user_instance = Users.objects.create(
                name="%s %s" % (patient_first_name, patient_last_name),
                mobile=mobile,
                email=email,
                account_type=keys.ACCOUNT_DOCTOR
            )
            patients_instance.user = user_instance

    patients_instance.patient_first_name = patient_first_name
    patients_instance.patient_last_name = patient_last_name
    patients_instance.occupation = occupation
    patients_instance.age = age
    patients_instance.gender = gender
    patients_instance.address = address
    patients_instance.city = city
    patients_instance.save()

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.PATIENT_TABLE_ID: patients_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def list_patient(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = PatientsData.objects.all().order_by('-id')

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

    patient_list = PatientsDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.PATIENT_LIST: patient_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def patient_details(request):
    patient_table_id = request.GET.get(keys.PATIENT_TABLE_ID, None)
    try:
        patients_instance = PatientsData.objects.get(id=patient_table_id)
    except PatientsData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    treatment_history = TreatmentRecordSerializer(
        TreatmentRecord.objects.filter(patient=patients_instance).order_by('-id'),
        many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.NAME: patients_instance.user.name,
        keys.MOBILE: patients_instance.user.mobile,
        keys.EMAIL: patients_instance.user.email,
        keys.GENDER: patients_instance.gender,
        keys.AGE: patients_instance.age,
        keys.OCCUPATION: patients_instance.occupation,
        keys.PATIENT_FIRST_NAME: patients_instance.patient_first_name,
        keys.PATIENT_LAST_NAME: patients_instance.patient_last_name,
        keys.ADDRESS: patients_instance.address,
        keys.CITY: patients_instance.city,
        keys.TREATMENT_HISTORY: treatment_history,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def get_treatment_history(request):
    treatment_table_id = request.GET.get(keys.TREATMENT_TABLE_ID, None)
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)
    from_date = request.GET.get(keys.FROM_DATE, None)
    to_date = request.GET.get(keys.TO_DATE, None)

    queryset = TreatmentRecord.objects.all().order_by('-id')
    if treatment_table_id:
        queryset = queryset.filter(id=treatment_table_id)

    if from_date and to_date:
        queryset = queryset.filter(created__date__gte=from_date, created__date__lte=to_date)
    if search_query:
        queryset = queryset.filter(
            Q(doctor__user__name__istartswith=search_query) |
            Q(patient__user__name__istartswith=search_query) |
            Q(patient__user__mobile__icontains=search_query) |
            Q(doctor__user__mobile__icontains=search_query) |
            Q(patient__user__email__icontains=search_query))

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    treatment_history = TreatmentRecordSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.TREATMENT_HISTORY: treatment_history,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def add_prescription(request):
    treatment_table_id = request.data.get(keys.TREATMENT_TABLE_ID, None)
    patient_table_id = request.data.get(keys.PATIENT_TABLE_ID, None)

    chief_complaint = request.data.get(keys.CHIEF_COMPLAINT, None)
    history_of_chief_complaint = request.data.get(keys.HISTORY_OF_CHIEF_COMPLAINT, None)
    blood_pressure = request.data.get(keys.BLOOD_PRESSURE, None)
    blood_sugar = request.data.get(keys.BLOOD_SUGAR, None)
    plus_rate = request.data.get(keys.PLUS_RATE, None)
    spo2 = request.data.get(keys.SPO2, None)
    temperature = request.data.get(keys.TEMPERATURE, None)
    oe = request.data.get(keys.OE, None)
    advise = request.data.get(keys.ADVISE, None)
    required_test = request.data.get(keys.REQUIRED_TEST, None)
    prescription_list = request.data.get(keys.PRESCRIPTION_LIST, None)

    user = HelperAuthentication.get_users_instance(request)

    if user.account_type == keys.ACCOUNT_DOCTOR:
        try:
            doctor = DoctorsData.objects.get(user=user)
        except DoctorsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.DOCTOR_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.DOCTOR_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    if patient_table_id:
        try:
            patient_instance = PatientsData.objects.get(id=patient_table_id)
        except PatientsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

    if treatment_table_id:
        try:
            treatment_instance = TreatmentRecord.objects.get(id=patient_table_id)
        except PatientsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        treatment_instance = TreatmentRecord()

    treatment_instance.doctor = doctor
    treatment_instance.patient = patient_instance
    treatment_instance.chief_complaint = chief_complaint
    treatment_instance.history_of_chief_complaint = history_of_chief_complaint

    treatment_instance.blood_pressure = blood_pressure
    treatment_instance.blood_sugar = blood_sugar
    treatment_instance.plus_rate = plus_rate
    treatment_instance.spo2 = spo2
    treatment_instance.temperature = temperature
    treatment_instance.oe = oe
    treatment_instance.required_test = required_test
    treatment_instance.advise = advise
    treatment_instance.required_test = required_test
    treatment_instance.save()

    if prescription_list and isinstance(prescription_list, str):
        prescription_list = json.loads(prescription_list)
        if prescription_list:
            for item in prescription_list:
                try:
                    drug_instance = DrugData.objects.get(id=item['drug'])
                    PrescriptionRecord.objects.create(
                        treatment_record=treatment_instance,
                        drug=drug_instance,
                        dose=item['dose'],
                        frequency=item['frequency'],
                        qty=item['qty'],
                        instruction=item['instruction'],
                    )
                except DrugData.DoesNotExist:
                    return Response({
                        keys.SUCCESS: False,
                        keys.MESSAGE: messages.DOCTOR_NOT_FOUND
                    }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TREATMENT_TABLE_ID: treatment_instance.id,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@CustomDjangoDecorators.validate_access_token
def delete_treatment_record(request):
    treatment_table_id = request.data.get(keys.TREATMENT_TABLE_ID, None)
    if treatment_table_id:
        try:
            treatment_instance = TreatmentRecord.objects.get(id=treatment_table_id)
            treatment_instance.delete()
        except PatientsData.DoesNotExist:
            return Response({
                keys.SUCCESS: False,
                keys.MESSAGE: messages.RECORD_NOT_FOUND
            }, status=status.HTTP_400_BAD_REQUEST)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def get_prescription_details(request):
    treatment_table_id = request.GET.get(keys.TREATMENT_TABLE_ID, None)

    dose_list = MaterDoseData.objects.filter().values_list('dose', flat=True)
    frequency_list = MaterFrequencyData.objects.filter().values_list('frequency', flat=True)
    instruction_list = MaterInstructionData.objects.filter().values_list('instruction', flat=True)
    try:
        treatment_instance = TreatmentRecord.objects.get(id=treatment_table_id)
    except TreatmentRecord.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    prescription_list = PrescriptionRecord.objects.filter(treatment_record=treatment_instance)
    prescription_list = PrescriptionRecordSerializer(prescription_list, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DOCTOR_NAME: treatment_instance.doctor.user.name,
        keys.TREATMENT_DATE: treatment_instance.created.strftime(keys.DATE_TIME_FORMAT),
        # patient
        keys.PATIENT_NAME: treatment_instance.patient.user.name,
        keys.PATIENT_MOBILE: treatment_instance.patient.user.mobile,
        keys.PATIENT_EMAIL: treatment_instance.patient.user.email,
        keys.GENDER: treatment_instance.patient.gender,
        keys.AGE: treatment_instance.patient.age,
        keys.OCCUPATION: treatment_instance.patient.occupation,
        keys.ADDRESS: treatment_instance.patient.address,
        keys.CITY: treatment_instance.patient.city,
        # observation
        keys.BLOOD_PRESSURE: treatment_instance.blood_pressure,
        keys.BLOOD_SUGAR: treatment_instance.blood_sugar,
        keys.PLUS_RATE: treatment_instance.plus_rate,
        keys.TEMPERATURE: treatment_instance.temperature,
        keys.SPO2: treatment_instance.spo2,
        # treatment and complaint
        keys.CHIEF_COMPLAINT: treatment_instance.chief_complaint,
        keys.HISTORY_OF_CHIEF_COMPLAINT: treatment_instance.history_of_chief_complaint,
        keys.ADVISE: treatment_instance.advise,
        keys.OE: treatment_instance.oe,
        keys.REQUIRED_TEST: treatment_instance.required_test,
        # prescription data
        keys.PRESCRIPTION_LIST: prescription_list,
        # extra data
        keys.DOSE_LIST: dose_list,
        keys.FREQUENCY_LIST: frequency_list,
        keys.INSTRUCTION_LIST: instruction_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@CustomDjangoDecorators.validate_access_token
def get_prescription_supporting_data(request):
    dose_list = MaterDoseData.objects.filter().values_list('dose', flat=True)
    frequency_list = MaterFrequencyData.objects.filter().values_list('frequency', flat=True)
    instruction_list = MaterInstructionData.objects.filter().values_list('instruction', flat=True)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.DOSE_LIST: dose_list,
        keys.FREQUENCY_LIST: frequency_list,
        keys.INSTRUCTION_LIST: instruction_list,
    }
    return Response(response, status=status.HTTP_200_OK)
