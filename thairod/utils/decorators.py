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
