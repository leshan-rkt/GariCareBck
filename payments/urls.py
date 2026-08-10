from django.urls import path
from .views import InitiateSTKPushView, MpesaCallbackView, UserTransactionsView

urlpatterns = [
    path('stk-push/', InitiateSTKPushView.as_view(), name='mpesa-stk-push'),
    path('callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('transactions/', UserTransactionsView.as_view(), name='user-transactions'),
]