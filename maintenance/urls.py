from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceRecordViewSet, CarTotalCostView

router = DefaultRouter()
router.register(r'', MaintenanceRecordViewSet, basename='maintenance')

urlpatterns = [
    path('', include(router.urls)),
    path('cost/<int:car_id>/', CarTotalCostView.as_view(), name='car-total-cost'),
]