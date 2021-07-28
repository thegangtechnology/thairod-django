from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, filters

from shipment.models import Shipment, TrackingStatus
from shipment.serializers.shipment_serializer import ShipmentSerializer
from shipment.serializers.tracking_status_serializer import TrackingStatusSerializer


class ShipmentModelViewSet(viewsets.ModelViewSet):
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status']


class TrackingStatusModelViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingStatusSerializer
    queryset = TrackingStatus.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code', 'status']


@csrf_exempt
def print_label(request: HttpRequest):
    shipment_id: str = request.GET.get("shipment_id", None)
    if shipment_id is None or shipment_id.isdigit():
        return HttpResponseBadRequest()
    # optimize this
    shipment = Shipment.objects.select_related().get(id=shipment_id)
    # purchase_id = shipment.shippop_purchase_id
    # receiver_name = shipment.order.receiver_name
    items = shipment.orderitem_set.select_related().all()
    for item in items:
        print(item.product_variation.name)
    if shipment is None:
        return HttpResponseBadRequest()
    return JsonResponse({'id': shipment_id})
