
from django.db.models import fields
from rest_framework import serializers
from .models import Vendor, purchaseOrder,Performance
 
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('vendor_id','name','contact_details','address','on_time_delivery_rate',
                    'quality_rating_avg','average_response_time','fulfillment_rate')

class purchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaseOrder
        fields = ('po_number','vendor','status','order_date','delivery_date','items',
                    'quality_rating','quantity','issue_date','acknowledgment_date')

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('vendor','date','on_time_delivery_rate','quality_rating_avg','average_response_time',
                    'fulfillment_rate')