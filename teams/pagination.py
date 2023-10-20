from rest_framework.pagination import PageNumberPagination


class ApiPagination(PageNumberPagination):
    """Adding pagination to endpoint pages"""
    page_size = 5
    max_page_size = 100
