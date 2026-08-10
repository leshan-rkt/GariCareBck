from rest_framework import serializers
from .models import MpesaTransaction

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = ['id', 'account_reference', 'amount', 'phone_number', 'status',
                  'mpesa_receipt_number', 'transaction_date', 'transaction_desc', 'created_at']
        read_only_fields = fields

class STKPushRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=1)
    account_reference = serializers.CharField(max_length=100)
    transaction_desc = serializers.CharField(max_length=255, required=False, default="Car Maintenance Payment")
    car_id = serializers.IntegerField(required=False, allow_null=True)
    maintenance_record_id = serializers.IntegerField(required=False, allow_null=True)