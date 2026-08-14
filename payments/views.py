from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from django_daraja.mpesa.core import MpesaClient
from .models import Payment
from maintenance.models import MaintenanceRecord

class InitiateSTKPushView(APIView):
    def post(self, request):
        try:
            # Get data from request
            maintenance_id = request.data.get('maintenance_id')
            phone = request.data.get('phone_number')
            amount = request.data.get('amount')
            account_reference = request.data.get('account_reference', 'Payment')

            # Clean phone number
            phone = phone.replace('+', '').replace(' ', '')
            if phone.startswith('0'):
                phone = '254' + phone[1:]

            # Initialize M-Pesa client
            cl = MpesaClient()

            # Call STK Push
            response = cl.stk_push(
                phone_number=phone,
                amount=int(amount),
                account_reference=account_reference,
                transaction_desc=f"Service Payment #{maintenance_id}",
                callback_url=settings.MPESA_CALLBACK_URL,
            )
            merchant_request_id = response.MerchantRequestID
            checkout_request_id = response.CheckoutRequestID
            message = response.ResponseDescription

            Payment.objects.create(
                maintenance_record_id=maintenance_id,
                payer_phone=phone,
                amount=amount,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                status='PENDING'
            )

            return Response({
                'success': True,
                'CheckoutRequestID': checkout_request_id,
                'MerchantRequestID': merchant_request_id,
                'message': message
            })

        except Exception as e:
            import traceback
            print("PAYMENT ERROR:", str(e))
            print(traceback.format_exc())
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# M-Pesa Callback View
class MpesaCallbackView(APIView):
    permission_classes = []  # Allow external calls from Safaricom

    def post(self, request):
        data = request.data
        checkout_id = data.get('CheckoutRequestID')
        result_code = data.get('ResultCode')
        result_desc = data.get('ResultDesc')

        # Update Payment record in database
        Payment.objects.filter(checkout_request_id=checkout_id).update(
            status='COMPLETED' if result_code == '0' else 'FAILED',
            result_code=result_code,
            result_desc=result_desc,
            mpesa_receipt=data.get('MpesaReceiptNumber', '')
        )
        return Response({"status": "ok"})
    
# Check Payment Status View
class CheckPaymentStatusView(APIView):
    def get(self, request, checkout_id):
        try:
            payment = Payment.objects.get(checkout_request_id=checkout_id)
            return Response({
                "status": payment.status,
                "receipt": payment.mpesa_receipt,
                "result_desc": payment.result_desc
            })
        except Payment.DoesNotExist:
            return Response({"status": "PENDING"}, status=404)