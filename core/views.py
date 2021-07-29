from rest_framework import viewsets


class MultiSerializersGenericViewSet(viewsets.GenericViewSet):
    """ To use multiple serializers for a view set, extends this class and define the following
    1. a dict named 'serializers' with keys as actions (str) and values as serializers
        e.g. serializers = {
            'list': QueryReviewSerializer
        }
    """
    serializers = {}

    def get_serializer_class(self):
        if self.action in self.serializers:
            return self.serializers[self.action]
        return super().get_serializer_class()  # use the default serializer e.g. serializer_class
