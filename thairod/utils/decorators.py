import functools
from typing import List

from django.http import HttpResponseForbidden

from thairod.utils.html_tools import get_client_ip


def swagger_example(example):
    """Decorate Serializer with this to add example to openapi doc

    Args:
        example (object): example object
    """

    def decorator(cls):
        if not hasattr(cls.Meta, 'swagger_schema_fields'):
            cls.Meta.swagger_schema_fields = {}
        cls.Meta.swagger_schema_fields["example"] = cls(example).data
        return cls

    return decorator


def ip_whitelist(ip_list: List[str]):
    def decorator(f):
        @functools.wraps(f)
        def ret(self, request, *arg, **kwds):
            ip = get_client_ip(request)

            if ip in ip_list:
                return f(self, request, *arg, **kwds)
            else:
                raise HttpResponseForbidden(f'Access Denied for {ip}')

        return ret

    return decorator

# https://youtrack.jetbrains.com/issue/PY-34569
# def auto_serialize(cls: T) -> T:
#     @swagger_example(cls.example())
#     class Serializer(DataclassSerializer[cls]):
#         class Meta:
#             dataclass = cls
#     cls.Serializer = Serializer
#     return cls
