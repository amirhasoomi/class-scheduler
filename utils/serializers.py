import six
# noinspection PyProtectedMember
from psycopg2._range import NumericRange
from rest_framework import serializers
from rest_framework.utils import json
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else:
            self.detail = {'detail': force_text(self.default_detail)}


class CurrentContextDefault:
    def __init__(self, key):
        self.key = key
        self.value = None

    def set_context(self, serializer_field):
        self.value = serializer_field.context[self.key]

    def __call__(self):
        return self.value

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class RangeSerializer(serializers.Field):
    """
    Expected input format:
        {
        "start": 49,
         "end": 24
        }
    """
    type_name = 'RangeField'
    type_label = 'range'

    default_error_messages = {
        'invalid': 'Enter a valid Range.',
    }

    def to_internal_value(self, value):
        """
        Parse json data and return a range object
        """
        if value in (None, '', [], (), {}) and not self.required:
            return None

        if isinstance(value, six.string_types):
            try:
                value = value.replace("'", '"')
                value = json.loads(value)
            except ValueError:
                self.fail('invalid')

        if value and isinstance(value, dict):
            try:
                return NumericRange(
                    int(value['lower']),
                    int(value['upper'])
                )
            except (TypeError, ValueError, KeyError):
                self.fail('invalid')
        self.fail('invalid')

    def to_representation(self, value):
        if isinstance(value, NumericRange):
            value = {
                "lower": value.lower,
                "upper": value.upper
            }
        return value
