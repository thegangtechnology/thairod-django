from rest_framework import serializers
from procurement.models import Procurement
from warehouse.models import Warehouse


class ProcurementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Procurement
        fields = '__all__'

    def create(self, validated_data):
        # drop any warehouse input.
        validated_data.pop('warehouse')
        # default warehouse for now.
        warehouse = Warehouse.objects.get(pk=1)
        procurement = Procurement.objects.create(warehouse=warehouse, **validated_data)
        procurement.save()
        return procurement
