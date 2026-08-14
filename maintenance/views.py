from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django.db.models import Sum, DecimalField
from .models import MaintenanceRecord
from .serializers import MaintenanceRecordSerializer


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['car', 'service_type', 'service_date']

    def get_queryset(self):
        return MaintenanceRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarTotalCostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, car_id):
        from cars.models import Car
        try:
            car = Car.objects.filter(user=request.user).get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found or not yours"}, status=404)

        records = MaintenanceRecord.objects.filter(user=request.user, car_id=car_id)
        total_cost = records.aggregate(total=Sum('cost', output_field=DecimalField()))['total'] or 0

        breakdown = records.values('service_type').annotate(
            subtotal=Sum('cost', output_field=DecimalField())
        )

        return Response({
            "car_id": car_id,
            "car": str(car),
            "total_maintenance_cost": float(total_cost),
            "total_records": records.count(),
            "cost_by_service_type": {item['service_type']: float(item['subtotal']) for item in breakdown}
        })