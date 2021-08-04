import os
from datetime import datetime

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from thairod.utils.html_tools import get_client_ip


class IPCheckView(APIView):
    permission_classes = [AllowAny]

    def timestamp(self) -> float:
        ts = os.path.getmtime(__file__)
        return ts

    def get(self, request, format=None):
        ts = self.timestamp()

        ret = {
            "ip": get_client_ip(request),
            "version-timestamp": ts,
            "version-datetime": datetime.fromtimestamp(ts)
        }
        return Response(ret)
