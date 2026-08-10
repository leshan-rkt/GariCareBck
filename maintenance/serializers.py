from rest_framework import serializers
from .models import MaintenanceRecord

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    car_details = serializers.CharField(source='car.__str__', read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = ['id', 'car', 'car_details', 'service_date', 'mileage_at_service',
                  'service_type', 'service_type_display', 'description',
                  'parts_replaced', 'cost', 'notes']
        read_only_fields = ['id']