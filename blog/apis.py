from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from .models import BlogData
from .serializers import BlogDataSerializer

Users = get_user_model()


@api_view(['GET'])
# @CustomDjangoDecorators.validate_access_token
def blog_list(request):
    page_number = request.GET.get(keys.PAGE_NUMBER, 1)
    page_length = request.GET.get(keys.PAGE_LENGTH, 20)
    search_query = request.GET.get(keys.SEARCH_QUERY, None)

    queryset = BlogData.objects.all().order_by('-id')

    # if search_query:

    paginator = Paginator(queryset, page_length)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    blog_list = BlogDataSerializer(queryset, many=True).data

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.TOTAL_PAGE_COUNT: paginator.num_pages,
        keys.BLOG_LIST: blog_list,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
# @CustomDjangoDecorators.validate_access_token
def blog_details(request):
    blog_table_id = request.GET.get(keys.BLOG_TABLE_ID, 1)

    try:
        blog_instance = BlogData.objects.get(id=blog_table_id)
    except BlogData.DoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.RECORD_NOT_FOUND
        }, status=status.HTTP_400_BAD_REQUEST)

    # blog_data = BlogDataSerializer(blog_instance, many=False).data
    suggestions = BlogData.objects.all().order_by('-id').exclude(id=blog_table_id)
    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.BLOG_DATA: blog_instance.blog_data,
        keys.SUGGESTIONS: BlogDataSerializer(suggestions[:3], many=True).data,
    }
    return Response(response, status=status.HTTP_200_OK)
