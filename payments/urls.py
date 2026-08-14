from django.urls import path
from .views import InitiateSTKPushView, MpesaCallbackView, CheckPaymentStatusView

urlpatterns = [
    path('stk-push/', InitiateSTKPushView.as_view(), name='stk-push'),
    path('callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('status/<str:checkout_id>/', CheckPaymentStatusView.as_view(), name='payment-status'),
]