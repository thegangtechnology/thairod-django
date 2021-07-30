from rest_framework.exceptions import APIException


class ShippopAPIException(APIException):
    status_code = 400
