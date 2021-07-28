from typing import TypeVar


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


# https://youtrack.jetbrains.com/issue/PY-34569
# def auto_serialize(cls: T) -> T:
#     @swagger_example(cls.example())
#     class Serializer(DataclassSerializer[cls]):
#         class Meta:
#             dataclass = cls
#     cls.Serializer = Serializer
#     return cls
