from rest_framework import serializers
from procurement.models import Procurement


class ProcurementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Procurement
        fields = '__all__'
