from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from django_daraja.mpesa.core import MpesaClient
from .models import MpesaTransaction
from .serializers import MpesaTransactionSerializer, STKPushRequestSerializer

# Create your views here.
class InitiateSTKPushView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = STKPushRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        phone = data['phone_number']
        if phone.startswith('0'): phone = '254' + phone[1:]
        elif phone.startswith('+'): phone = phone[1:]

        amount = int(data['amount'])
        callback_url = f"{settings.BASE_URL}/api/payments/callback/"

        try:
            cl = MpesaClient()
            response = cl.stk_push(phone, amount, data['account_reference'], data['transaction_desc'], callback_url)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        transaction = MpesaTransaction.objects.create(
            user=request.user,
            merchant_request_id=response.get('MerchantRequestID'),
            checkout_request_id=response.get('CheckoutRequestID'),
            amount=data['amount'],
            phone_number=phone,
            account_reference=data['account_reference'],
            transaction_desc=data.get('transaction_desc'),
            car_id=data.get('car_id'),
            maintenance_record_id=data.get('maintenance_record_id')
        )

        return Response({
            "success": True,
            "message": "Payment prompt sent — enter PIN on your phone",
            "transaction_id": transaction.id
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request):
        try:
            stk_result = request.data.get('Body', {}).get('stkCallback', {})
            checkout_req_id = stk_result.get('CheckoutRequestID')
            result_code = stk_result.get('ResultCode')
            result_desc = stk_result.get('ResultDesc')

            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_req_id)
            transaction.result_code = result_code
            transaction.result_desc = result_desc

            if result_code == 0:
                items = stk_result.get('CallbackMetadata', {}).get('Item', [])
                meta = {item['Name']: item.get('Value') for item in items}
                transaction.mpesa_receipt_number = meta.get('MpesaReceiptNumber')
                transaction.transaction_date = timezone.make_aware(
                    timezone.datetime.strptime(str(meta.get('TransactionDate')), "%Y%m%d%H%M%S")
                )
                transaction.status = MpesaTransaction.Status.COMPLETED
            else:
                transaction.status = MpesaTransaction.Status.FAILED

            transaction.save()
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

        except Exception as e:
            return JsonResponse({"ResultCode": 1, "ResultDesc": str(e)}, status=400)


class UserTransactionsView(generics.ListAPIView):
    serializer_class = MpesaTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MpesaTransaction.objects.filter(user=self.request.user)