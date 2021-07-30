from django.shortcuts import render
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from shipment.models import Shipment
from user.models import User


class TempAuth(authentication.BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        if userid == 'hello' and password == 'world':
            return User.objects.first(), None
        else:
            raise AuthenticationFailed('bad bad')


class SimpleShipmentListView(APIView):
    authentication_classes = [TempAuth]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        shipments = Shipment.objects.all()
        return render(request, "shipment_list.html", {
            "shipments": shipments
        })
