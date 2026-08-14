from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.MaintenanceRecordViewSet, basename='maintenance')

urlpatterns = [
    path('', include(router.urls)),
    path('car/<int:car_id>/total-cost/', views.CarTotalCostView.as_view(), name='car-total-cost'),
]