from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from secrets import token_hex
from rest_framework.serializers import Serializer


def gs(**kwargs):
    return type(token_hex(10), (Serializer,), kwargs)


class ExtraContextMixin:
    def get_serializer_context(self):
        # noinspection PyUnresolvedReferences
        context = super().get_serializer_context()
        context.update(self.extra_context())
        return context

    def extra_context(self):
        return {}


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 30

    def get_paginated_response(self, data):
        return Response({
            'num_of_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'data': data,
        })


class CustomOrderingFilter(OrderingFilter):
    def get_schema_fields(self, view):
        import coreapi
        import coreschema
        from django.utils.encoding import force_str
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'

        valid_fields = getattr(view, 'ordering_fields', None)
        default_fields = getattr(view, 'ordering', None)
        if valid_fields is not None:
            valid_fields = ', '.join(valid_fields)
        if default_fields is not None:
            if isinstance(default_fields, str):
                default_fields = (default_fields,)
            default_fields = ', '.join(default_fields)
        valid_fields = valid_fields or ''
        default_fields = default_fields or ''
        # noinspection PyArgumentList
        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.ordering_title),
                    description=f'choices: {valid_fields},\n default: {default_fields}'
                )
            )
        ]


def postman(schema):
    def _postman(request, token):
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        factory.get(path='/sagger/?format=openapi', format='json')
        new_request = factory.request()
        new_request.META['HTTP_AUTHORIZATION'] = f'Bearer {token.strip()}'
        return schema(new_request, format='openapi').render()

    return _postman
