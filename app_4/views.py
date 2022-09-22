from django.shortcuts import render
from .models import Student, Path
from .serializers import StudentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
# Create your views here.

from .pagination import SmallPageNumberPagination
from .pagination import MyLimitOffsetPagination
from .pagination import MyCursorPagination
from django_filters.rest_framework import DjangoFilterBackend # for filter.
from rest_framework.filters import SearchFilter, OrderingFilter# for search


class StudentMVS(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = SmallPageNumberPagination
    # pagination_class = MyLimitOffsetPagination
    # pagination_class = MyCursorPagination
    filter_backends = [DjangoFilterBackend, SearchFilter,  OrderingFilter] #local ayar, settings eklemeden
    filterset_fields = ['first_name', 'last_name', 'number']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name']


    def get_queryset(self):
        queryset = self.queryset
        path = self.request.query_params.get('path')
        if path is not None:
            mypath = Path.objects.get(path_name=path)
            queryset = queryset.filter(path=mypath.id)
        return queryset   
    
    



    @action(detail= False, methods = ["GET"])
    def student_count(self, request):
        count = {
            "student-count":self.queryset.count()
        }

        return Response(count)