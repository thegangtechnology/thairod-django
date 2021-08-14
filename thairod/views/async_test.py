from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from thairod.tasks import test_celery


class AsyncView(APIView):
    def get(self, request: Request) -> Response:
        s = test_celery.delay()
        return Response({'msg': s.get(timeout=5)})
