from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.views import APIView

from shipment.models import Shipment


class SimpleShipmentListView(APIView):

    def get(self, request: Request):
        shipments = Shipment.objects.all()
        return render(request, "shipment_list.html", {
            "shipments": shipments
        })
