import functools
import logging
from typing import List

from django.http import HttpResponseForbidden

from thairod.settings import DEBUG
from thairod.utils.html_tools import get_client_ip

logger = logging.getLogger(__name__)


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


def ip_whitelist(ip_list: List[str], allow_all_if_debug=False):
    def decorator(f):
        @functools.wraps(f)
        def ret(self, request, *arg, **kwds):
            ip = get_client_ip(request)
            allow_while_debug = DEBUG and allow_all_if_debug
            if allow_while_debug or ip in ip_list:
                return f(self, request, *arg, **kwds)
            else:
                msg = f'Access Denied for {ip}'
                logger.warning(msg)
                return HttpResponseForbidden(msg)

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
