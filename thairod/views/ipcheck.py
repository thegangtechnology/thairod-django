from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from thairod.utils.html_tools import get_client_ip


class IPCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        ip = {"ip": get_client_ip(request)}
        return Response(ip)
