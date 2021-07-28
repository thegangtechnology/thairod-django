import functools
from typing import Type, Generic, TypeVar, Dict, Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_dataclasses.serializers import DataclassSerializer

from thairod.utils.decorators import swagger_example

T = TypeVar('T')


class TGSerializer(DataclassSerializer[T], Generic[T]):
    def parse_request(cls, request: Request) -> T:
        raise NotImplementedError()


class AutoSerialize:

    def to_response(self) -> Response:
        return Response(self.to_data())

    def to_data(self) -> Dict[str, Any]:
        return self.__class__.serializer()(self).data

    @classmethod
    def from_data(cls: Type[T], data: Dict[str, Any]) -> T:
        ser = cls.serializer()(data=data)
        ser.is_valid(raise_exception=True)
        return ser.save()

    @classmethod
    def from_request(cls: Type[T], request: Request) -> T:
        return cls.from_data(request.data)

    @classmethod
    @functools.lru_cache
    def serializer(cls: Type[T]) -> Type[TGSerializer[T]]:

        class Serializer(TGSerializer[cls]):
            class Meta:
                dataclass = cls
                ref_name = cls.__name__

            @classmethod
            def parse_request(cls, request: Request) -> T:
                ser = cls(data=request.data)
                ser.is_valid(raise_exception=True)
                return ser.save()

        if hasattr(cls, 'example') and callable(cls.example):
            return swagger_example(cls.example())(Serializer)
        else:
            return Serializer


def swagger_auto_serialize_schema(body_type: Type[AutoSerialize], response_type: Type[AutoSerialize]):
    return swagger_auto_schema(
        request_body=body_type.serializer(),
        responses={200: response_type.serializer()}
    )
