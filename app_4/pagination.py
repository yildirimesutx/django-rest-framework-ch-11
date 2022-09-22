from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination


# PageNumberPagination classını inherit ediyoruz ve yeni class farklı isimlendirebiliriz
# page_size bu inherit edilen class in attributi 
class SmallPageNumberPagination(PageNumberPagination):
    page_size = 8


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3    


# CursorPagination Local Settings:
from rest_framework.pagination import CursorPagination
class MyCursorPagination(CursorPagination):
    page_size = 10
    ordering = "number"  